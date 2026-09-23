from odoo import _, models
from odoo.exceptions import UserError


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    def do_scrap(self):
        if not self.env.user.has_group('almx_stock_movement_guard.group_direccion'):
            raise UserError(_(
                "🚫 Solo Dirección puede desechar material.\n\n"
                "Si el material está dañado, crea una transferencia interna hacia la "
                "ubicación de Merma y usa \"Solicitar autorización\"."
            ))
        return super().do_scrap()
