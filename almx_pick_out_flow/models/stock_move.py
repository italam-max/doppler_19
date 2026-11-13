from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _skip_push(self):
        # El OUT de un PICK ya no se genera al validar el PICK: lo crea el botón
        # "Crear OUT" (action_create_related_out), que llama _push_apply directo.
        if len(self) == 1 and self.picking_type_id \
                and self.picking_type_id == self.picking_type_id.warehouse_id.pick_type_id:
            return True
        return super()._skip_push()
