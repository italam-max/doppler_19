from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _almx_sol_frozen(self):
        """Líneas de productos almacenables de una SO confirmada: su cantidad y
        producto definen lo que sale en la OUT congelada."""
        return self.filtered(lambda l: l.order_id.state == 'sale' and l.product_id.is_storable)

    def _almx_raise_frozen(self, order):
        raise UserError(_(
            "🚫 El pedido %(so)s ya está confirmado: no se pueden agregar, quitar ni "
            "cambiar productos o cantidades de artículos de inventario.\n\n"
            "Si el pedido está mal, cancélalo y genera uno nuevo.", so=order.name))

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        if not self.env.su:
            frozen = lines._almx_sol_frozen()
            if frozen:
                self._almx_raise_frozen(frozen[0].order_id)
        return lines

    def write(self, vals):
        if not self.env.su and ({'product_id', 'product_uom_qty', 'product_uom_id'} & set(vals)):
            frozen = self._almx_sol_frozen()
            if 'product_id' in vals and not frozen:
                # cambiar un servicio por un almacenable en SO confirmada también cuenta
                frozen = self.filtered(lambda l: l.order_id.state == 'sale') if \
                    self.env['product.product'].browse(vals['product_id']).is_storable else frozen
            if frozen:
                self._almx_raise_frozen(frozen[0].order_id)
        return super().write(vals)

    def unlink(self):
        if not self.env.su:
            frozen = self._almx_sol_frozen()
            if frozen:
                self._almx_raise_frozen(frozen[0].order_id)
        return super().unlink()
