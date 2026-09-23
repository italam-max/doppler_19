from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    is_available = fields.Boolean(
        string='Hay stock',
        compute='_compute_is_available',
        help="False si lo reservado para el movimiento no cubre su demanda "
             "completa (falta stock). No se guarda en BD.",
    )

    @api.depends('quantity', 'move_id.quantity', 'move_id.product_uom_qty', 'state', 'location_id')
    def _compute_is_available(self):
        """En 19 la cantidad de la línea ES la reserva. Se evalúa el
        movimiento completo (suma de sus líneas vs demanda): así un
        movimiento repartido en varios lotes no se ve rojo solo porque
        cada línea individual es menor a la demanda total."""
        for line in self:
            move = line.move_id
            if (line.state in ('done', 'cancel')
                    or line.location_id.usage != 'internal'
                    or not move or not move.product_uom_qty):
                line.is_available = True
                continue
            line.is_available = move.product_uom.compare(move.quantity, move.product_uom_qty) >= 0
