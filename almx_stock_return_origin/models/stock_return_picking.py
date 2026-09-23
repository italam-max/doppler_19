# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import Command, models


class StockReturnPickingLine(models.TransientModel):
    _inherit = 'stock.return.picking.line'

    def _almx_pick_origins(self):
        """Ubicaciones físicas reales de donde salió el producto en el PICK
        que surtió al movimiento devuelto (sube un nivel por move_orig_ids).

        Devuelve [(stock.location, cantidad_en_UdM_del_move_devuelto)], de
        mayor a menor. Lista vacía si no hay PICK encadenado (se conserva el
        comportamiento estándar). Se descartan ubicaciones archivadas: regresar
        mercancía ahí la esconde de los reportes normales.
        """
        self.ensure_one()
        origin_move = self.move_id
        if not origin_move:
            return []
        pick_moves = origin_move.move_orig_ids.filtered(
            lambda m: m.picking_type_id.code == 'internal' and m.state == 'done'
        )
        if not pick_moves:
            return []
        uom = origin_move.product_uom
        qty_per_loc = defaultdict(float)
        for line in pick_moves.move_line_ids.filtered(lambda l: l.state == 'done'):
            qty = line.product_uom_id._compute_quantity(line.quantity, uom)
            if qty > 0 and line.location_id.active and line.location_id.usage == 'internal':
                qty_per_loc[line.location_id] += qty
        return sorted(qty_per_loc.items(), key=lambda x: x[1], reverse=True)

    def _almx_allocation(self):
        """Reparte self.quantity entre las ubicaciones de origen: llena primero
        la de mayor cantidad hasta lo que salió de ahí, luego la siguiente.
        Si se devuelve más de lo que registró el PICK, el excedente va a la
        principal. Devuelve [(location, qty)] sin cantidades en cero."""
        self.ensure_one()
        origins = self._almx_pick_origins()
        if not origins:
            return []
        uom = self.uom_id
        remaining = self.quantity
        alloc = []
        for loc, qty in origins:
            if uom.compare(remaining, 0) <= 0:
                break
            take = min(remaining, qty)
            alloc.append([loc, take])
            remaining -= take
        if uom.compare(remaining, 0) > 0:
            alloc[0][1] += remaining
        return [(loc, qty) for loc, qty in alloc if uom.compare(qty, 0) > 0]

    def _prepare_move_default_values(self, new_picking):
        vals = super()._prepare_move_default_values(new_picking)
        alloc = self._almx_allocation()
        if alloc:
            vals['location_dest_id'] = alloc[0][0].id
            vals['product_uom_qty'] = alloc[0][1]
        return vals

    def _process_line(self, new_picking):
        alloc = self._almx_allocation()
        before = new_picking.move_ids
        res = super()._process_line(new_picking)
        if res and len(alloc) > 1:
            new_move = (new_picking.move_ids - before).filtered(
                lambda m: m.origin_returned_move_id == self.move_id)[:1]
            if new_move:
                for loc, qty in alloc[1:]:
                    new_move.copy({
                        'product_uom_qty': qty,
                        'location_dest_id': loc.id,
                        'picking_id': new_picking.id,
                        'origin_returned_move_id': self.move_id.id,
                        'move_orig_ids': [Command.set(new_move.move_orig_ids.ids)],
                        'move_dest_ids': [Command.set(new_move.move_dest_ids.ids)],
                        'location_final_id': False,
                        'state': 'draft',
                    })
        return res


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _prepare_picking_default_values(self):
        """El encabezado se decide antes de crear los moves: en 19, escribir
        location_dest_id del picking reescribe el de todos sus moves."""
        vals = super()._prepare_picking_default_values()
        locs = self.env['stock.location']
        for line in self.product_return_moves.filtered(lambda l: l.quantity > 0):
            for loc, _qty in line._almx_allocation():
                locs |= loc
        if len(locs) == 1:
            vals['location_dest_id'] = locs.id
        elif len(locs) > 1:
            common = None
            for loc in locs:
                path = [int(x) for x in loc.parent_path.split('/') if x]
                common = path if common is None else [a for a, b in zip(common, path) if a == b]
            parent = self.env['stock.location'].browse(common[-1]) if common else locs.browse()
            if parent and parent.usage == 'internal':
                vals['location_dest_id'] = parent.id
        return vals
