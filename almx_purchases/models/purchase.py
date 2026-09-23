from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    almx_is_import = fields.Boolean(
        string='Importación',
        compute='_compute_almx_is_import', store=True, readonly=False, precompute=True,
        tracking=True,
        help='Compra de importación: sus recepciones requieren número de pedimento.',
    )

    @api.depends('partner_id')
    def _compute_almx_is_import(self):
        for order in self:
            order.almx_is_import = order.partner_id.commercial_partner_id.almx_import_vendor
