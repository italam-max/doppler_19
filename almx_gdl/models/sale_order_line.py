# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Almacén 2 y Almacén 3 son las ubicaciones de resguardo real en CDMX
    # (Almacén 1 es de entrega y Almacén 4 no se usa, excluidos a propósito);
    # GDL/Existencias es la única de GDL. No almacenados: se calculan al
    # momento y no hacen crecer la base de datos.
    x_stock_alm2 = fields.Float(
        string='Stock Almacén 2', compute='_compute_stock_por_ubicacion', digits='Product Unit',
        help='Cantidad disponible en Almacén 2 (CDMX) al momento de consultar.')
    x_stock_alm3 = fields.Float(
        string='Stock Almacén 3', compute='_compute_stock_por_ubicacion', digits='Product Unit',
        help='Cantidad disponible en Almacén 3 (CDMX) al momento de consultar.')
    x_stock_gdl = fields.Float(
        string='Stock GDL', compute='_compute_stock_por_ubicacion', digits='Product Unit',
        help='Cantidad disponible en GDL/Existencias al momento de consultar.')
    x_almacenes_disponibles_ids = fields.Many2many(
        'stock.location', compute='_compute_stock_por_ubicacion',
        string='Almacenes con existencia',
        help='Ubicaciones (Almacén 2, Almacén 3, GDL/Existencias) con existencia '
             'disponible del producto; limita lo que se puede elegir en Almacén de Retirada.')

    x_almacen_retirada_id = fields.Many2one(
        'stock.location', string='Almacén de Retirada',
        domain="[('id', 'in', x_almacenes_disponibles_ids)]",
        help='De dónde se va a surtir esta línea. Solo aparecen las ubicaciones con '
             'existencia disponible del producto. GDL agrega la ruta de entrega de GDL '
             '(1 paso); Almacén 2 o 3 sigue el flujo default de CDMX (PICK + OUT). '
             'No dispara traslados ni reabastos automáticos.')

    # ------------------------------------------------------------------
    @api.model
    def _get_location_ids_validacion(self):
        icp = self.env['ir.config_parameter'].sudo()
        return (
            int(icp.get_param('sale_multi_warehouse_validation.location_alm2_id', default=1519)),
            int(icp.get_param('sale_multi_warehouse_validation.location_alm3_id', default=1520)),
            int(icp.get_param('sale_multi_warehouse_validation.location_gdl_id', default=3600)),
        )

    @api.model
    def _get_route_gdl(self):
        icp = self.env['ir.config_parameter'].sudo()
        return self.env['stock.route'].browse(
            int(icp.get_param('sale_multi_warehouse_validation.route_gdl_id', default=131))).exists()

    @api.depends('product_id')
    def _compute_stock_por_ubicacion(self):
        Location = self.env['stock.location']
        Quant = self.env['stock.quant']
        loc_alm2, loc_alm3, loc_gdl = (Location.browse(i) for i in self._get_location_ids_validacion())
        for line in self:
            product = line.product_id
            if not product or not product.is_storable:
                line.x_stock_alm2 = line.x_stock_alm3 = line.x_stock_gdl = 0.0
                line.x_almacenes_disponibles_ids = Location
                continue
            qtys = {
                loc_alm2: Quant._get_available_quantity(product, loc_alm2),
                loc_alm3: Quant._get_available_quantity(product, loc_alm3),
                loc_gdl: Quant._get_available_quantity(product, loc_gdl),
            }
            line.x_stock_alm2 = qtys[loc_alm2]
            line.x_stock_alm3 = qtys[loc_alm3]
            line.x_stock_gdl = qtys[loc_gdl]
            uom = product.uom_id
            line.x_almacenes_disponibles_ids = Location.union(
                *[loc for loc, q in qtys.items() if uom.compare(q, 0.0) > 0])

    @api.onchange('product_id')
    def _onchange_product_id_reset_almacen_retirada(self):
        # Si cambia el producto, la ubicación elegida puede ya no tener
        # existencia: se limpia (y se quita la ruta de GDL) para forzar a
        # elegir de nuevo.
        route_gdl = self._get_route_gdl()
        for line in self:
            if line.x_almacen_retirada_id:
                line.x_almacen_retirada_id = False
                line.route_ids -= route_gdl

    @api.onchange('x_almacen_retirada_id')
    def _onchange_almacen_retirada_id(self):
        loc_gdl = self._get_location_ids_validacion()[2]
        route_gdl = self._get_route_gdl()
        for line in self:
            if line.x_almacen_retirada_id.id == loc_gdl and route_gdl:
                line.route_ids |= route_gdl
            else:
                # Almacén 2/3 o sin selección -> flujo default de CDMX. Solo se
                # quita la ruta de GDL; nunca se agrega la de reabasto (134).
                line.route_ids -= route_gdl

    @api.constrains('x_almacen_retirada_id', 'product_id')
    def _check_almacen_retirada_tiene_stock(self):
        # Respaldo server-side del dominio de la vista (aplica también por RPC).
        for line in self:
            if line.x_almacen_retirada_id and line.x_almacen_retirada_id not in line.x_almacenes_disponibles_ids:
                raise ValidationError(_(
                    "No se puede elegir '%(ubicacion)s' como Almacén de Retirada para "
                    "'%(producto)s' porque ahí no hay existencia disponible de ese producto "
                    "en este momento. Eso generaría una salida en negativo.",
                    ubicacion=line.x_almacen_retirada_id.display_name,
                    producto=line.product_id.display_name,
                ))
