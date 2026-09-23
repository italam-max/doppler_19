# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # Solo para la vista: oculta la serie pre-reservada cuando el producto
    # es de seguimiento por SERIE (no lote) y el tipo de operación exige
    # confirmación manual.
    almx_hide_lot = fields.Boolean(
        string='Ocultar número de serie (candado manual)',
        compute='_compute_almx_hide_lot',
    )

    @api.depends('product_id.tracking', 'picking_type_id.require_serial_confirmation')
    def _compute_almx_hide_lot(self):
        for line in self:
            line.almx_hide_lot = bool(
                line.product_id.tracking == 'serial'
                and line.picking_type_id.require_serial_confirmation
            )
