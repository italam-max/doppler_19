from odoo import api, fields, models, _
from odoo.exceptions import AccessError

PRICE_GROUP = 'almx_lunch_price.group_lunch_price_editor'


class LunchOrder(models.Model):
    _inherit = 'lunch.order'
    price = fields.Monetary(readonly=False)

    can_edit_price = fields.Boolean(compute='_compute_can_edit_price')

    @api.depends_context('uid')
    def _compute_can_edit_price(self):
        can_edit = self.env.user.has_group(PRICE_GROUP)
        for order in self:
            order.can_edit_price = can_edit

    def write(self, vals):

        if 'price' in vals and not self.env.su and not self.env.user.has_group(PRICE_GROUP):
            raise AccessError(_(
                "No tienes permiso para modificar el precio de los pedidos de almuerzo. "
                "Solicita pertenecer al grupo «Editor de precios de almuerzo»."
            ))
        return super().write(vals)
