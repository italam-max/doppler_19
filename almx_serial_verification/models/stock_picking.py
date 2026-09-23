# -*- coding: utf-8 -*-
from odoo import _, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    almx_require_serial_confirmation = fields.Boolean(
        related='picking_type_id.require_serial_confirmation',
    )

    def button_validate(self):
        if not self.env.context.get('almx_serial_confirmed'):
            action = self._almx_maybe_open_serial_wizard()
            if action:
                return action
        return super().button_validate()

    def _almx_serial_lines_to_confirm(self):
        """Líneas de producto con serie que Odoo 19 realmente va a procesar:
        si hay movimientos marcados como 'picked', solo esos; si no, todos."""
        lines = self.env['stock.move.line']
        for picking in self.filtered('picking_type_id.require_serial_confirmation'):
            moves = picking.move_ids.filtered(lambda m: m.state not in ('done', 'cancel'))
            moves = moves.filtered('picked') or moves
            lines |= moves.move_line_ids.filtered(
                lambda l: l.product_id.tracking == 'serial'
                and not l.product_uom_id.is_zero(l.quantity)
            )
        return lines

    def _almx_maybe_open_serial_wizard(self):
        lines = self._almx_serial_lines_to_confirm()
        if not lines:
            return False
        wizard = self.env['almx.serial.confirm.wizard'].create({
            'picking_ids': [(6, 0, lines.picking_id.ids)],
            'line_ids': [(0, 0, {'move_line_id': line.id}) for line in lines],
        })
        return {
            'name': _('Confirmar números de serie'),
            'type': 'ir.actions.act_window',
            'res_model': 'almx.serial.confirm.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }
