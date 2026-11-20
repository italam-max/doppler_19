from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Se leen de la venta (sin copia) para que PICK y OUT muestren siempre lo mismo, desde que se abren.
    almx_carrier_id = fields.Many2one(related='sale_id.carrier_id', string='Método de entrega')
    almx_collect_date = fields.Datetime(related='sale_id.collect_date', string='Fecha de recolección')
    almx_shipping_address = fields.Char(related='sale_id.partner_shipping_id.contact_address',
                                        string='Dirección de entrega')
    almx_shipping_kind = fields.Selection(related='sale_id.carrier_id.almx_shipping_kind', string='Tipo de método')
    almx_paqueteria = fields.Selection(related='sale_id.almx_paqueteria')
    almx_paqueteria_otra = fields.Char(related='sale_id.almx_paqueteria_otra')
    almx_tipo_servicio = fields.Selection(related='sale_id.almx_tipo_servicio')
    almx_sucursal_destino = fields.Char(related='sale_id.almx_sucursal_destino')
    almx_contacto_nombre = fields.Char(related='sale_id.almx_contacto_nombre')
    almx_contacto_telefono = fields.Char(related='sale_id.almx_contacto_telefono')
    almx_app_servicio = fields.Selection(related='sale_id.almx_app_servicio')
    almx_app_otra = fields.Char(related='sale_id.almx_app_otra')
    almx_app_referencia = fields.Char(related='sale_id.almx_app_referencia')

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super().create(vals_list)
        pickings._almx_sync_carrier_from_sale()
        return pickings

    def _almx_sync_carrier_from_sale(self):
        """Copia el método de la venta al traslado abierto (para listas, filtros y reportes)."""
        for picking in self:
            sale = picking.sale_id
            if sale and picking.state not in ('done', 'cancel') and picking.carrier_id != sale.carrier_id:
                picking.carrier_id = sale.carrier_id
