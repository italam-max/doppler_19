# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    returned_qty = fields.Float(
        string='Cantidad devuelta',
        compute='_compute_returned_qty',
        help='Cantidad de este producto que ya se devolvió (movimientos de '
             'devolución en estado done que apuntan a este movimiento vía '
             'origin_returned_move_id).',
    )

    def _compute_returned_qty(self):
        return_moves = self.env['stock.move'].search([
            ('origin_returned_move_id', 'in', self.ids),
            ('state', '=', 'done'),
        ])
        qty_by_origin = {}
        for rm in return_moves:
            origin_id = rm.origin_returned_move_id.id
            qty_by_origin[origin_id] = qty_by_origin.get(origin_id, 0.0) + rm.quantity
        for move in self:
            move.returned_qty = qty_by_origin.get(move.id, 0.0)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    return_ids = fields.Many2many(
        'stock.picking', string='Devoluciones', compute='_compute_return_ids',
        help='Devoluciones (documentos NWH/RET/...) generadas a partir de '
             'algún movimiento de esta transferencia, incluyendo intentos '
             'cancelados (visibles en la columna de estado de la lista).',
    )
    return_count = fields.Integer(
        string='# Devoluciones', compute='_compute_return_ids',
        help='Número total de devoluciones asociadas a esta transferencia, '
             'incluyendo canceladas -- el estado de cada una se ve al '
             'entrar a la lista.',
    )

    def _compute_return_ids(self):
        for picking in self:
            move_ids = picking.move_ids.ids
            return_moves = self.env['stock.move'].search([
                ('origin_returned_move_id', 'in', move_ids),
            ]) if move_ids else self.env['stock.move']
            return_pickings = return_moves.picking_id
            picking.return_ids = return_pickings
            picking.return_count = len(return_pickings)

    def action_view_returns(self):
        self.ensure_one()
        action = {
            'name': 'Devoluciones',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'context': {'create': False},
        }
        if len(self.return_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.return_ids.id,
            })
        else:
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', 'in', self.return_ids.ids)],
            })
        return action
