from odoo import _, api, fields, models
from odoo.exceptions import UserError

# Evidencia de surtido: se captura en el PICK y se refleja en el OUT ligado.
ALMX_PICK_URL_FIELDS = (
    'x_studio_evidencia_fotogrfica',  # URL Almacén
    'x_studio_url_bodega',            # URL Bodega
    'x_studio_url_laboratorio',       # URL Laboratorio
    'x_studio_url_calidad',           # URL Calidad
)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # ---------------------------------------------------------------- PICK / OUT
    almx_is_pick = fields.Boolean(compute='_compute_almx_is_pick')
    almx_has_out = fields.Boolean(compute='_compute_almx_has_out')
    almx_require_comprobante = fields.Boolean(related='picking_type_id.almx_require_comprobante')
    almx_comprobante_user_id = fields.Many2one('res.users', string='Comprobante subido por', copy=False, readonly=True)
    almx_comprobante_date = fields.Datetime(string='Comprobante subido el', copy=False, readonly=True)
    almx_source_pick_id = fields.Many2one('stock.picking', compute='_compute_almx_source_pick_id')
    almx_lock_url_almacen = fields.Boolean(compute='_compute_almx_lock_urls')
    almx_lock_url_bodega = fields.Boolean(compute='_compute_almx_lock_urls')
    almx_lock_url_laboratorio = fields.Boolean(compute='_compute_almx_lock_urls')
    almx_lock_url_calidad = fields.Boolean(compute='_compute_almx_lock_urls')

    @api.depends('picking_type_id')
    def _compute_almx_is_pick(self):
        for picking in self:
            picking.almx_is_pick = picking._almx_is_pick_type()

    def _almx_is_pick_type(self):
        self.ensure_one()
        ptype = self.picking_type_id
        return bool(ptype and ptype.code == 'internal' and ptype.warehouse_id.pick_type_id == ptype)

    @api.depends('related_out_id.state', 'move_ids.move_dest_ids.picking_id.state')
    def _compute_almx_has_out(self):
        for picking in self:
            picking.almx_has_out = bool(picking._almx_existing_outs())

    def _almx_existing_outs(self):
        """OUT no cancelados ligados al PICK (incluye backorders)."""
        self.ensure_one()
        outs = self.related_out_id | self.move_ids.move_dest_ids.picking_id
        return outs.filtered(lambda p: p.picking_type_code == 'outgoing' and p.state != 'cancel')

    @api.depends('related_pick_id', 'move_ids.move_orig_ids.picking_id', 'picking_type_code')
    def _compute_almx_source_pick_id(self):
        for picking in self:
            pick = self.env['stock.picking']
            if picking.picking_type_code == 'outgoing':
                pick = picking.related_pick_id
                if not pick:
                    pick = picking.move_ids.move_orig_ids.picking_id.filtered(lambda p: p._almx_is_pick_type())[:1]
            picking.almx_source_pick_id = pick

    @api.depends('almx_source_pick_id', *('almx_source_pick_id.%s' % f for f in ALMX_PICK_URL_FIELDS))
    def _compute_almx_lock_urls(self):
        for picking in self:
            pick = picking.almx_source_pick_id
            picking.almx_lock_url_almacen = bool(pick.x_studio_evidencia_fotogrfica)
            picking.almx_lock_url_bodega = bool(pick.x_studio_url_bodega)
            picking.almx_lock_url_laboratorio = bool(pick.x_studio_url_laboratorio)
            picking.almx_lock_url_calidad = bool(pick.x_studio_url_calidad)

    def _almx_get_target_outs(self):
        """OUT(s) abiertos ligados a este PICK."""
        self.ensure_one()
        outs = self.related_out_id
        if not outs:
            outs = self.move_ids.move_dest_ids.picking_id.filtered(lambda p: p.picking_type_code == 'outgoing')
        return outs.filtered(lambda p: p.state not in ('done', 'cancel'))

    def _almx_sync_urls_to_out(self, only_filled=False):
        for pick in self.filtered(lambda p: p._almx_is_pick_type()):
            vals = {f: pick[f] for f in ALMX_PICK_URL_FIELDS if not only_filled or pick[f]}
            outs = pick._almx_get_target_outs()
            if vals and outs:
                outs.sudo().with_context(almx_url_sync=True).write(vals)

    def write(self, vals):
        if vals.get('x_studio_comprobante') and 'almx_comprobante_user_id' not in vals:
            vals = dict(vals, almx_comprobante_user_id=self.env.user.id, almx_comprobante_date=fields.Datetime.now())
        res = super().write(vals)
        if self.env.context.get('almx_url_sync'):
            return res
        if any(f in vals for f in ALMX_PICK_URL_FIELDS):
            self._almx_sync_urls_to_out()
        # El vínculo PICK↔OUT se puede crear después: se llenan los valores que ya traiga el PICK.
        if 'related_out_id' in vals:
            self._almx_sync_urls_to_out(only_filled=True)
        if 'related_pick_id' in vals:
            self.related_pick_id._almx_sync_urls_to_out(only_filled=True)
        return res

    # ------------------------------------------------------------- Crear OUT
    def action_create_related_out(self):
        self.ensure_one()
        if not self.env.su and not self.env.user.has_group('almx_stock_extends.group_almx_manual_out_creator'):
            raise UserError(_('No tienes permiso para crear el OUT. Solicítalo a Dirección o a TI.'))
        if not self._almx_is_pick_type():
            raise UserError(_('El OUT solo se puede crear desde un PICK.'))
        if self.state != 'done':
            raise UserError(_('El OUT solo se puede crear cuando el PICK %s ya está validado.', self.name))
        outs = self._almx_existing_outs()
        if outs:
            raise UserError(_('El PICK %(pick)s ya tiene OUT: %(outs)s', pick=self.name, outs=', '.join(outs.mapped('name'))))

        # Esquema nuevo: el PICK nació de la venta con destino final Clientes.
        # Se aplica la regla push nativa Almacén 1 → Clientes (conserva línea de venta y encadenamiento).
        push_moves = self.move_ids.filtered(
            lambda m: m.state == 'done' and m.quantity and not m.move_dest_ids
            and m.location_final_id.usage == 'customer'
        )
        if not push_moves:
            # PICK del esquema anterior sin OUT: método original de almx_stock_extends.
            return super().action_create_related_out()

        new_moves = push_moves.with_context(almx_create_out=True)._push_apply()
        out = new_moves.picking_id.filtered(lambda p: p.picking_type_code == 'outgoing')[:1]
        if not out:
            raise UserError(_('No se pudo crear el OUT: falta la regla de salida Almacén 1 → Clientes. Avisa a TI.'))
        new_moves._action_assign()
        out.related_pick_id = self.id
        self.related_out_id = out.id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Salida generada'),
            'res_model': 'stock.picking',
            'res_id': out.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # ------------------------------------------------- Comprobante de entrega
    def _almx_missing_comprobante(self):
        return self.filtered(
            lambda p: p.almx_require_comprobante and not p.x_studio_comprobante and p.state not in ('done', 'cancel')
        )

    def _pre_action_done_hook(self):
        # Corre después de los candados de button_validate y antes del asistente de backorder.
        if not self.env.context.get('almx_skip_comprobante'):
            missing = self._almx_missing_comprobante()
            if len(missing) > 1:
                raise UserError(_(
                    'Estas entregas no tienen Comprobante. Valídalas una por una para subir cada uno:\n%s',
                    '\n'.join(missing.mapped('name')),
                ))
            if missing:
                ctx = {k: v for k, v in self.env.context.items() if not k.startswith('default_')}
                ctx['almx_comprobante_picking_id'] = missing.id
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Comprobante de entrega'),
                    'res_model': 'almx.comprobante.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': ctx,
                }
        return super()._pre_action_done_hook()

    def _action_done(self):
        # Respaldo por si algún flujo valida sin pasar por el botón Validar.
        if not self.env.context.get('almx_skip_comprobante'):
            missing = self._almx_missing_comprobante()
            if missing:
                raise UserError(_('No se puede validar sin Comprobante: %s', ', '.join(missing.mapped('name'))))
        return super()._action_done()
