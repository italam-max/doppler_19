# -*- coding: utf-8 -*-
import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError

SO_PATTERN = re.compile(r'\bSO\d+\b', re.IGNORECASE)


class AlmxPurchaseSaleCopy(models.TransientModel):
    _name = 'almx.purchase.sale.copy'
    _description = 'Copiar equipo de la venta a la compra'

    purchase_id = fields.Many2one('purchase.order', readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string='Proveedor',
        help='Proveedor de la nueva solicitud de compra (solo al crear la PO desde la venta).')
    sale_ref = fields.Char(string='Venta (SO)', required=True)
    sale_info = fields.Char(string='Venta encontrada', readonly=True)
    line_ids = fields.One2many('almx.purchase.sale.copy.line', 'wizard_id', string='Productos')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        po = self.env['purchase.order'].browse(res.get('purchase_id') or self.env.context.get('default_purchase_id'))
        if po and 'sale_ref' in fields_list and not res.get('sale_ref'):
            match = SO_PATTERN.search(' '.join(filter(None, [po.partner_ref, po.origin])))
            if match:
                res['sale_ref'] = match.group(0).upper()
        return res

    def _almx_find_sale(self):
        """La mayoría de Compras no tiene acceso a Ventas: se busca con sudo y
        solo se exponen productos, cantidades y descripciones."""
        self.ensure_one()
        ref = (self.sale_ref or '').strip().upper()
        if not ref:
            return self.env['sale.order']
        company = self.purchase_id.company_id or self.env.company
        # sudo: sale.order - lectura de la venta de referencia para usuarios de Compras
        return self.env['sale.order'].sudo().search(
            [('name', '=', ref), ('company_id', '=', company.id), ('state', '!=', 'cancel')], limit=1)

    @api.onchange('sale_ref')
    def _onchange_sale_ref(self):
        sale = self._almx_find_sale()
        commands = [fields.Command.clear()]
        if not sale:
            self.sale_info = _('No se encontró la venta') if self.sale_ref else False
            self.line_ids = commands
            return
        if sale.sale_type != 'project':
            self.sale_info = _('%s no es de Equipo Nuevo', sale.name)
            self.line_ids = commands
            return
        self.sale_info = '%s - %s' % (sale.partner_id.display_name, sale.date_order.strftime('%d/%m/%Y') if sale.date_order else '')
        for sline in sale.order_line.filtered(lambda l: not l.display_type and l.product_id):
            product = sline.product_id
            custom = '\n'.join(
                '%s: %s' % (c.custom_product_template_attribute_value_id.display_name, c.custom_value or '')
                for c in sline.product_custom_attribute_value_ids
            )
            commands.append(fields.Command.create({
                'selected': product.type != 'service' and product.purchase_ok,
                'sale_line_ref': sline.id,
                'product_id': product.id,
                'product_uom_qty': sline.product_uom_qty,
                'uom_id': sline.product_uom_id.id,
                'description': sline.name,
                'no_variant_ptav_ids': [fields.Command.set(sline.product_no_variant_attribute_value_ids.ids)],
                'custom_text': custom,
            }))
        self.line_ids = commands

    def action_apply(self):
        self.ensure_one()
        sale = self._almx_find_sale()
        if not sale:
            raise UserError(_('No se encontró la venta %s.', self.sale_ref or ''))
        if sale.sale_type != 'project':
            raise UserError(_('%s no es de Equipo Nuevo: solo se copian ventas de Equipo Nuevo.', sale.name))
        po = self.purchase_id
        create_mode = not po
        if create_mode and not self.partner_id:
            raise UserError(_('Selecciona el proveedor de la solicitud de compra.'))
        if po and po.state not in ('draft', 'sent'):
            raise UserError(_('Solo se pueden agregar productos a solicitudes de cotización (borrador o enviadas).'))
        selected = self.line_ids.filtered('selected')
        if not selected:
            raise UserError(_('Selecciona al menos un producto.'))
        not_purchasable = selected.filtered(lambda l: not l.product_id.purchase_ok)
        if not_purchasable:
            raise UserError(_('Estos productos no están marcados como "Se puede comprar":\n%s',
                              '\n'.join(not_purchasable.product_id.mapped('display_name'))))
        if create_mode:
            po = self.env['purchase.order'].create({
                'partner_id': self.partner_id.id,
                'company_id': sale.company_id.id,
                'origin': sale.name,
            })
        vals_list = []
        for line in selected:
            product = line.product_id
            qty = line.product_uom_qty
            if line.uom_id and line.uom_id != product.uom_id:
                qty = line.uom_id._compute_quantity(qty, product.uom_id)
            vals_list.append({
                'order_id': po.id,
                'product_id': product.id,
                'product_qty': qty,
                'product_no_variant_attribute_value_ids': [fields.Command.set(line.no_variant_ptav_ids.ids)],
            })
        new_lines = self.env['purchase.order.line'].create(vals_list)
        for po_line, line in zip(new_lines, selected):
            if line.custom_text:
                po_line.name = '%s\n%s' % (po_line.name, line.custom_text)
        if sale.name not in (po.origin or ''):
            po.origin = ', '.join(filter(None, [po.origin, sale.name]))
        if create_mode:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'res_id': po.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return {'type': 'ir.actions.act_window_close'}


class AlmxPurchaseSaleCopyLine(models.TransientModel):
    _name = 'almx.purchase.sale.copy.line'
    _description = 'Línea a copiar de la venta'

    wizard_id = fields.Many2one('almx.purchase.sale.copy', required=True, ondelete='cascade')
    selected = fields.Boolean(string='Copiar', default=True)
    sale_line_ref = fields.Integer()
    product_id = fields.Many2one('product.product', string='Producto', required=True)
    description = fields.Text(string='Descripción en la venta')
    product_uom_qty = fields.Float(string='Cantidad')
    uom_id = fields.Many2one('uom.uom', string='Unidad')
    no_variant_ptav_ids = fields.Many2many(
        'product.template.attribute.value', 'almx_pur_sale_copy_line_ptav_rel', 'line_id', 'ptav_id')
    custom_text = fields.Text()
