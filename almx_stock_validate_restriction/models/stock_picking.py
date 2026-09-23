import logging

from markupsafe import Markup

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _svr_moves_to_process(self):
        """Movimientos que Odoo 19 realmente va a procesar al validar:
        si hay alguno marcado como 'picked', solo esos; si no hay ninguno,
        Odoo marca todos (ver _pre_action_done_hook)."""
        self.ensure_one()
        moves = self.move_ids.filtered(lambda m: m.state not in ('done', 'cancel'))
        picked = moves.filtered('picked')
        return picked or moves

    # ------------------------------------------------------------------
    # Regla 1: consistencia PICK -> OUT
    # ------------------------------------------------------------------
    def _check_pick_before_out(self):
        for picking in self.filtered(lambda p: p.picking_type_code == 'outgoing'):
            for move in picking._svr_moves_to_process():
                if not move.move_orig_ids:
                    continue
                uom = move.product_uom
                # Lo recolectado de verdad en el paso previo
                picked_ready = sum(
                    m.product_uom._compute_quantity(m.quantity, uom)
                    for m in move.move_orig_ids if m.state == 'done'
                )
                # Lo que ya salió en otras OUT (backorders) del mismo PICK
                already_sent = sum(
                    m.product_uom._compute_quantity(m.quantity, uom)
                    for m in move.move_orig_ids.move_dest_ids
                    if m.state == 'done' and m != move
                )
                available_from_pick = picked_ready - already_sent
                sending_now = move.quantity

                if uom.compare(sending_now, available_from_pick) > 0:
                    origins = ', '.join(sorted(set(move.move_orig_ids.picking_id.mapped('name'))))
                    raise UserError(_(
                        "🚫 ERROR DE CONSISTENCIA\n\n"
                        "Estás intentando validar la salida de %(sending).2f %(uom)s de '%(product)s',\n"
                        "pero del paso anterior (PICK) solo hay %(ready).2f %(uom)s disponibles "
                        "(recolectado: %(picked).2f, ya enviado en otras salidas: %(sent).2f).\n\n"
                        "Documentos origen: %(origins)s\n"
                        "Solución: no puedes enviar material que no ha sido recolectado (pickeado).",
                        sending=sending_now, uom=uom.name, product=move.product_id.display_name,
                        ready=available_from_pick, picked=picked_ready, sent=already_sent,
                        origins=origins or '-',
                    ))

    # ------------------------------------------------------------------
    # Regla 2: candado anti-negativos
    # ------------------------------------------------------------------
    def _prevent_negative_stock(self):
        """Recorta la cantidad de las líneas cuando excede el físico real de
        la ubicación de origen menos lo reservado por OTRAS transferencias.

        En 19 la cantidad de cada línea ya está reservada en el quant
        (reserved_quantity), incluso si el usuario la subió a mano por
        encima de lo disponible. Por eso:

            físico_para_este_grupo = (quantity - reserved_quantity del quant,
                                      SIN recortar a 0: allow_negative=True)
                                     + lo que el propio grupo tiene en líneas

        Se agrupan las líneas que comparten quant (producto/ubicación/lote/
        paquete/dueño) para no dejar pasar dos líneas que por separado
        "ven" el total completo.

        No aplica a ubicaciones no internas (proveedores, clientes,
        producción, ajustes). Misma limitación de concurrencia que en 16:
        no hay bloqueo de fila; dos validaciones simultáneas del mismo
        quant pueden colarse.
        """
        Quant = self.env['stock.quant']
        MoveLine = self.env['stock.move.line']

        lines = MoveLine
        for picking in self:
            lines |= picking._svr_moves_to_process().move_line_ids
        lines = lines.filtered(
            lambda l: l.product_id.is_storable
            and l.location_id.usage == 'internal'
            and not l.product_uom_id.is_zero(l.quantity)
        )
        if not lines:
            return

        groups = {}
        for line in lines:
            key = (line.product_id.id, line.location_id.id, line.lot_id.id,
                   line.package_id.id, line.owner_id.id)
            groups.setdefault(key, MoveLine)
            groups[key] |= line

        for group in groups.values():
            sample = group[0]
            product_uom = sample.product_id.uom_id
            free_qty = Quant._get_available_quantity(
                sample.product_id, sample.location_id,
                lot_id=sample.lot_id, package_id=sample.package_id,
                owner_id=sample.owner_id, strict=True, allow_negative=True,
            )
            group_qty = sum(group.mapped('quantity_product_uom'))
            physical = max(free_qty + group_qty, 0.0)

            if product_uom.compare(group_qty, physical) <= 0:
                continue

            remaining = physical  # en UdM del producto
            for line in group.sorted(key=lambda l: -l.quantity_product_uom):
                original = line.quantity
                original_pu = line.quantity_product_uom
                allowed_pu = max(min(original_pu, remaining), 0.0)
                remaining -= allowed_pu
                if product_uom.compare(allowed_pu, original_pu) == 0:
                    continue
                adjusted = product_uom._compute_quantity(
                    allowed_pu, line.product_uom_id, rounding_method='DOWN')
                line.quantity = adjusted
                line.picking_id.message_post(body=Markup(_(
                    "⚠️ Ajuste automático por falta de stock: <b>%(product)s</b> se "
                    "redujo de %(original)s a %(adjusted)s %(uom)s en %(location)s. "
                    "La diferencia quedará pendiente (backorder)."
                )) % {
                    'product': line.product_id.display_name, 'original': original,
                    'adjusted': adjusted, 'uom': line.product_uom_id.name,
                    'location': line.location_id.display_name,
                })

    def _check_not_all_zero(self):
        for picking in self:
            moves = picking._svr_moves_to_process()
            if moves and all(m.product_uom.is_zero(m.quantity) for m in moves):
                raise UserError(_(
                    "🚫 No se puede validar '%(name)s': no hay stock físico disponible "
                    "para ninguno de sus productos en la ubicación de origen.\n\n"
                    "Esto no se puede forzar tecleando una cantidad manualmente: "
                    "el candado anti-negativos la va a volver a bajar a 0. "
                    "Verifica las existencias reales antes de continuar.",
                    name=picking.name,
                ))

    # ------------------------------------------------------------------
    # Regla 3: encadenar la OUT al validar el PICK
    # ------------------------------------------------------------------
    def _chain_related_out(self):
        for picking in self.filtered(lambda p: p.picking_type_code == 'internal' and p.state == 'done'):
            out = picking.related_out_id
            if not out or out.state in ('done', 'cancel') or out.products_availability_state != 'available':
                continue
            try:
                with self.env.cr.savepoint():
                    res = out.button_validate()
                if isinstance(res, dict) or out.state != 'done':
                    out.message_post(body=_(
                        "La validación automática desde %(pick)s requiere confirmación "
                        "manual; valida esta salida directamente.", pick=picking.name))
            except UserError as e:
                _logger.info("Auto-validación de %s desde %s no procedió: %s", out.name, picking.name, e)
                out.message_post(body=_(
                    "No se pudo validar automáticamente desde %(pick)s: %(err)s",
                    pick=picking.name, err=str(e)))

    # ------------------------------------------------------------------
    def button_validate(self):
        self._check_pick_before_out()
        self._prevent_negative_stock()
        self._check_not_all_zero()
        res = super().button_validate()
        self._chain_related_out()
        return res
