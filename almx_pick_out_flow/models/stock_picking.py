from odoo import api, fields, models

# Evidencia de surtido: se captura en el PICK y se refleja en el OUT ligado.
ALMX_PICK_URL_FIELDS = (
    'x_studio_evidencia_fotogrfica',  # URL Almacén
    'x_studio_url_bodega',            # URL Bodega
    'x_studio_url_laboratorio',       # URL Laboratorio
)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # ---------------------------------------------------------------- PICK / OUT
    almx_is_pick = fields.Boolean(compute='_compute_almx_is_pick')
    almx_source_pick_id = fields.Many2one('stock.picking', compute='_compute_almx_source_pick_id')
    almx_lock_url_almacen = fields.Boolean(compute='_compute_almx_lock_urls')
    almx_lock_url_bodega = fields.Boolean(compute='_compute_almx_lock_urls')
    almx_lock_url_laboratorio = fields.Boolean(compute='_compute_almx_lock_urls')

    @api.depends('picking_type_id')
    def _compute_almx_is_pick(self):
        for picking in self:
            picking.almx_is_pick = picking._almx_is_pick_type()

    def _almx_is_pick_type(self):
        self.ensure_one()
        ptype = self.picking_type_id
        return bool(ptype and ptype.code == 'internal' and ptype.warehouse_id.pick_type_id == ptype)

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
