from odoo import _, api, fields, models
from odoo.exceptions import UserError

GROUP_DIRECCION = 'almx_stock_movement_guard.group_direccion'
GROUP_ASSET = 'almx_stock_movement_guard.group_asset_assignment'


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    almx_require_sale_order = fields.Boolean(related='picking_type_id.almx_require_sale_order')
    almx_direction_reason = fields.Char(
        string='Requiere autorización de Dirección',
        compute='_compute_almx_direction_reason',
        help='Motivo por el que este traslado solo lo puede validar Dirección.',
    )
    almx_is_direccion = fields.Boolean(compute='_compute_almx_is_direccion')

    # ------------------------------------------------------------------
    @api.depends_context('uid')
    def _compute_almx_is_direccion(self):
        is_dir = self.env.user.has_group(GROUP_DIRECCION)
        for picking in self:
            picking.almx_is_direccion = is_dir

    @api.depends('state', 'picking_type_id', 'location_dest_id',
                 'move_ids.location_dest_id', 'move_line_ids.location_dest_id',
                 'move_ids.purchase_line_id', 'move_ids.origin_returned_move_id')
    def _compute_almx_direction_reason(self):
        for picking in self:
            picking.almx_direction_reason = '; '.join(picking._almx_direction_reasons()) or False

    # ------------------------------------------------------------------
    def _almx_active_moves(self):
        self.ensure_one()
        return self.move_ids.filtered(lambda m: m.state != 'cancel')

    def _almx_direction_reasons(self):
        """Motivos por los que SOLO Dirección puede validar este traslado."""
        self.ensure_one()
        reasons = []
        if self.state in ('done', 'cancel'):
            return reasons

        # Destino en ubicación marcada (Merma / Laboratorio / Desecho)
        flagged = self.env['stock.location'].sudo().search([('almx_requires_direction', '=', True)])
        if flagged:
            dests = (self.location_dest_id
                     | self._almx_active_moves().location_dest_id
                     | self.move_line_ids.location_dest_id)
            hit = dests.filtered_domain([('id', 'child_of', flagged.ids)])
            if hit:
                reasons.append(_('destino %s', ', '.join(hit.mapped('display_name'))))

        # Recepción sin Orden de compra ni devolución nativa
        if self.picking_type_code == 'incoming' and self.picking_type_id.almx_guard_receipts:
            moves = self._almx_active_moves()
            from_po = moves and all(m.purchase_line_id for m in moves)
            is_return = moves and all(m.origin_returned_move_id for m in moves)
            if not (from_po or is_return):
                reasons.append(_('recepción sin Orden de compra ni devolución'))
        return reasons

    def _almx_check_guards(self):
        user = self.env.user
        is_dir = user.has_group(GROUP_DIRECCION)
        for picking in self:
            ptype = picking.picking_type_id

            # 1. Pedido de venta obligatorio
            moves = picking._almx_active_moves()
            is_native_return = bool(moves) and all(m.origin_returned_move_id for m in moves)
            if ptype.almx_require_sale_order and not is_native_return:
                so = picking.sale_id
                if not so:
                    raise UserError(_(
                        "🚫 '%(name)s' no tiene Pedido de venta ligado.\n\n"
                        "Todo movimiento de este tipo debe salir con una SO. Captura el "
                        "Pedido de venta en el encabezado del traslado.",
                        name=picking.name))
                if so.state != 'sale':
                    raise UserError(_(
                        "🚫 El Pedido de venta %(so)s de '%(name)s' no está confirmado.",
                        so=so.name, name=picking.name))

            # 2. Solo Dirección (Merma / Laboratorio / Desecho / IN sin documento)
            reasons = picking._almx_direction_reasons()
            if reasons and not is_dir:
                raise UserError(_(
                    "🚫 '%(name)s' solo lo puede validar Dirección (%(reasons)s).\n\n"
                    "Usa el botón \"Solicitar autorización\" para avisarles.",
                    name=picking.name, reasons='; '.join(reasons)))

            # 3. Asignación de equipo: solo TI / RH y solo a ubicaciones de asignación
            if ptype.almx_asset_assignment:
                if not (is_dir or user.has_group(GROUP_ASSET)):
                    raise UserError(_(
                        "🚫 Solo TI y RH pueden validar asignaciones de equipo ('%(name)s').",
                        name=picking.name))
                allowed = self.env['stock.location'].sudo().search([('almx_asset_location', '=', True)])
                dests = (picking.location_dest_id
                         | picking._almx_active_moves().location_dest_id
                         | picking.move_line_ids.location_dest_id)
                bad = dests - (dests.filtered_domain([('id', 'child_of', allowed.ids)]) if allowed else dests.browse())
                if bad:
                    raise UserError(_(
                        "🚫 '%(name)s' es una asignación de equipo, pero tiene destino fuera "
                        "de las ubicaciones de asignación: %(locs)s.",
                        name=picking.name, locs=', '.join(bad.mapped('display_name'))))

    def button_validate(self):
        self._almx_check_guards()
        return super().button_validate()

    # ------------------------------------------------------------------
    def action_almx_request_direction(self):
        users = self.env.ref(GROUP_DIRECCION).sudo().user_ids.filtered('active')
        if not users:
            raise UserError(_("No hay usuarios en el grupo Dirección."))
        for picking in self:
            reasons = picking._almx_direction_reasons()
            if not reasons:
                raise UserError(_("'%(name)s' no requiere autorización de Dirección.", name=picking.name))
            for u in users:
                picking.activity_schedule(
                    'mail.mail_activity_data_todo', user_id=u.id,
                    summary=_('Autorizar y validar %s', picking.name),
                    note=_('Solicitado por %(who)s: %(reasons)s',
                           who=self.env.user.name, reasons='; '.join(reasons)),
                )
            picking.message_post(body=_(
                "Se solicitó autorización de Dirección (%(reasons)s).", reasons='; '.join(reasons)))
        return True

    @api.onchange('sale_id')
    def _onchange_almx_sale_id(self):
        so = self.sale_id
        if not so:
            return
        self.origin = so.name
        shipping = so.partner_shipping_id or so.partner_id
        if shipping:
            self.partner_id = shipping
            if 'partner_only_dir' in self._fields:
                self.partner_only_dir = so.partner_shipping_id
