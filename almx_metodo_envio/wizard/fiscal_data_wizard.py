from odoo import _, api, fields, models
from odoo.exceptions import UserError


def _sale_selection(field_name):
    return lambda self: self.env['sale.order']._fields[field_name]._description_selection(self.env)


class AlmxFiscalDataWizard(models.TransientModel):
    _name = 'almx.fiscal.data.wizard'
    _inherit = ['almx.fiscal.capture.mixin']
    _description = 'Datos fiscales del cliente y forma de emitir la factura'

    order_id = fields.Many2one('sale.order', string='Venta', required=True, ondelete='cascade')
    inv_usage = fields.Selection(selection=_sale_selection('l10n_mx_edi_usage'), string='Uso del CFDI')
    inv_payment_method_id = fields.Many2one('l10n_mx_edi.payment.method', string='Forma de pago')
    inv_payment_policy = fields.Selection(selection=_sale_selection('l10n_mx_edi_payment_policy'),
                                          string='Método de pago (PUE / PPD)')
    inv_cfdi_to_public = fields.Boolean(string='CFDI a público en general')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        order = self.env['sale.order'].browse(res.get('order_id') or self.env.context.get('default_order_id'))
        if order:
            res.update(self._fis_defaults(order.partner_id))
            res.update({
                'inv_usage': order.l10n_mx_edi_usage,
                'inv_payment_method_id': order.l10n_mx_edi_payment_method_id.id,
                'inv_payment_policy': order.l10n_mx_edi_payment_policy,
                'inv_cfdi_to_public': order.l10n_mx_edi_cfdi_to_public,
            })
        return res

    def action_apply(self):
        self.ensure_one()
        missing = self._fis_missing()
        if not self.inv_usage:
            missing.append(_('Uso del CFDI'))
        if not self.inv_payment_method_id:
            missing.append(_('Forma de pago'))
        if not self.inv_payment_policy:
            missing.append(_('Método de pago (PUE / PPD)'))
        if missing:
            raise UserError(_('Falta información para la factura:\n\n%s') % '\n'.join('• %s' % m for m in missing))
        self._fis_apply()
        self.order_id.write({
            'l10n_mx_edi_usage': self.inv_usage,
            'l10n_mx_edi_payment_method_id': self.inv_payment_method_id.id,
            'l10n_mx_edi_payment_policy': self.inv_payment_policy,
            'l10n_mx_edi_cfdi_to_public': self.inv_cfdi_to_public,
        })
        return {'type': 'ir.actions.act_window_close'}
