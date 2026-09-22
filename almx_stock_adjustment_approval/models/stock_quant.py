# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_apply_inventory(self):
        if self.env.context.get('bypass_adjustment_approval'):
            return super().action_apply_inventory()

        if self.env.user.has_group('almx_stock_adjustment_approval.group_stock_adjustment_approver'):
            return super().action_apply_inventory()

        quants_con_diferencia = self.filtered(
            lambda q: q.inventory_quantity_set and q.inventory_diff_quantity != 0
        )
        if not quants_con_diferencia:
            raise UserError(_(
                'No hay diferencias de inventario que ajustar. '
                'Verifica que hayas ingresado las cantidades contadas.'
            ))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Solicitar Aprobación de Ajuste'),
            'res_model': 'stock.adjustment.request.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_quant_ids': quants_con_diferencia.ids,
                'active_ids': quants_con_diferencia.ids,
            },
        }
