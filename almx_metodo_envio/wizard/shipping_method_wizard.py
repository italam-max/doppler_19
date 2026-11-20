from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..models.sale_order import (
    ADDRESS_KINDS, ALL_SHIPPING_FIELDS, APPS, FISCAL_REQUIRED, KIND_FIELDS, LEGACY_RECOLECCION_NAME,
    PAQUETERIAS, TIPOS_SERVICIO, almx_shipping_core_missing,
)


class AlmxShippingMethodWizard(models.TransientModel):
    _name = 'almx.shipping.method.wizard'
    _inherit = ['almx.address.capture.mixin', 'almx.fiscal.capture.mixin']
    _description = 'Captura del método de envío de la venta'

    order_id = fields.Many2one('sale.order', string='Venta', required=True, ondelete='cascade')
    sale_type = fields.Selection(related='order_id.sale_type')
    carrier_id = fields.Many2one('delivery.carrier', string='Método de envío')
    almx_shipping_kind = fields.Selection(related='carrier_id.almx_shipping_kind')
    collect_date = fields.Datetime(string='Fecha y hora de recolección')
    almx_paqueteria = fields.Selection(PAQUETERIAS, string='Paquetería')
    almx_paqueteria_otra = fields.Char(string='Otra paquetería')
    almx_tipo_servicio = fields.Selection(TIPOS_SERVICIO, string='Tipo de servicio')
    almx_sucursal_destino = fields.Char(string='Sucursal destino')
    almx_contacto_nombre = fields.Char(string='Contacto de entrega')
    almx_contacto_telefono = fields.Char(string='Teléfono de contacto')
    almx_app_servicio = fields.Selection(APPS, string='App de envío')
    almx_app_otra = fields.Char(string='Otra app')
    almx_app_referencia = fields.Char(string='Referencia / placas')
    from_select = fields.Boolean(default=lambda self: bool(self.env.context.get('almx_from_select')))
    needs_address = fields.Boolean(compute='_compute_needs')
    needs_fiscal = fields.Boolean(compute='_compute_needs')

    @api.depends('carrier_id', 'almx_paqueteria')
    def _compute_needs(self):
        for wiz in self:
            kind = wiz.carrier_id.almx_shipping_kind
            wiz.needs_address = kind in ADDRESS_KINDS
            wiz.needs_fiscal = kind == 'paqueteria' and wiz.almx_paqueteria in FISCAL_REQUIRED

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order = self.env['sale.order'].browse(res.get('order_id') or self.env.context.get('default_order_id'))
        if order:
            res.update(self._addr_defaults(order))
            res.update(self._fis_defaults(order.partner_id))
            if order.carrier_id.almx_shipping_kind:
                res['carrier_id'] = order.carrier_id.id
                res['collect_date'] = order.collect_date
                for fname in ALL_SHIPPING_FIELDS:
                    res[fname] = order[fname]
        return res

    @api.onchange('carrier_id')
    def _onchange_carrier_id(self):
        keep = KIND_FIELDS.get(self.carrier_id.almx_shipping_kind, ())
        for fname in ALL_SHIPPING_FIELDS:
            if fname not in keep:
                self[fname] = False
        if self.carrier_id.almx_shipping_kind != 'recoleccion':
            self.collect_date = False

    def action_apply(self):
        self.ensure_one()
        order = self.order_id
        if not self.carrier_id:
            raise UserError(_('Elige el método de envío.'))
        kind = self.carrier_id.almx_shipping_kind
        missing = almx_shipping_core_missing(self, kind, order.sale_type)
        if self.needs_address:
            missing += self._addr_missing()
        if self.needs_fiscal:
            missing += self._fis_missing()
        if missing:
            raise UserError(_('Falta información para guardar el método de envío:\n\n%s')
                            % '\n'.join('• %s' % m for m in missing))
        if self.needs_fiscal:
            self._fis_apply()
        is_immediate = kind == 'recoleccion' or (not kind and self.carrier_id.name == LEGACY_RECOLECCION_NAME)
        vals = {
            'carrier_id': self.carrier_id.id,
            'is_immediate': is_immediate,
            'collect_date': self.collect_date if is_immediate else False,
        }
        keep = KIND_FIELDS.get(kind, ())
        for fname in ALL_SHIPPING_FIELDS:
            vals[fname] = self[fname] if fname in keep else False
        if vals.get('almx_paqueteria') != 'otra':
            vals['almx_paqueteria_otra'] = False
        if vals.get('almx_tipo_servicio') != 'ocurre':
            vals['almx_sucursal_destino'] = False
        if vals.get('almx_app_servicio') != 'otra':
            vals['almx_app_otra'] = False
        if self.needs_address:
            vals['partner_shipping_id'] = self._addr_resolve().id
        order.write(vals)
        if self.env.context.get('almx_confirm_after'):
            ctx = {k: v for k, v in self.env.context.items()
                   if not k.startswith('default_') and k != 'almx_confirm_after'}
            ctx.update(validate_analytic=True, almx_confirm_ui=True)
            res = order.with_context(ctx).action_confirm()
            if isinstance(res, dict):
                return res
        return {'type': 'ir.actions.act_window_close'}
