from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AlmxShippingAddressWizard(models.TransientModel):
    _name = 'almx.shipping.address.wizard'
    _inherit = ['almx.address.capture.mixin']
    _description = 'Cambio de dirección de entrega de la venta'

    order_id = fields.Many2one('sale.order', string='Venta', required=True, ondelete='cascade')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order = self.env['sale.order'].browse(res.get('order_id') or self.env.context.get('default_order_id'))
        if order:
            res.update(self._addr_defaults(order))
        return res

    def action_apply(self):
        self.ensure_one()
        missing = self._addr_missing()
        if missing:
            raise UserError(_('Falta información de la dirección de entrega:\n\n%s')
                            % '\n'.join('• %s' % m for m in missing))
        self.order_id.write({'partner_shipping_id': self._addr_resolve().id})
        return {'type': 'ir.actions.act_window_close'}
