# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from markupsafe import escape
import json


class StockAdjustmentRequestWizard(models.TransientModel):
    _name = 'stock.adjustment.request.wizard'
    _description = 'Wizard - Solicitud de Aprobación de Ajuste de Inventario'

    reason = fields.Text(
        string='Motivo del Ajuste',
        required=True,
    )
    quant_ids_context = fields.Text(
        string='Quant IDs (contexto)',
        default=lambda self: json.dumps(self.env.context.get('default_quant_ids', [])),
    )
    adjustment_preview = fields.Html(
        string='Detalle del Ajuste a Solicitar',
        compute='_compute_preview',
        sanitize=False,
    )

    @api.depends('quant_ids_context')
    def _compute_preview(self):
        for rec in self:
            try:
                ids = json.loads(rec.quant_ids_context or '[]')
                quants = self.env['stock.quant'].browse(ids)
                rows = ''
                for q in quants:
                    diff = q.inventory_diff_quantity
                    color = 'red' if diff < 0 else 'green'
                    rows += f'''<tr>
                        <td style="padding:4px 8px;">{escape(q.product_id.display_name)}</td>
                        <td style="padding:4px 8px;">{escape(q.location_id.complete_name)}</td>
                        <td style="padding:4px 8px; text-align:right;">{q.quantity:.2f}</td>
                        <td style="padding:4px 8px; text-align:right;">{q.inventory_quantity:.2f}</td>
                        <td style="padding:4px 8px; text-align:right; color:{color};">{diff:+.2f}</td>
                        <td style="padding:4px 8px;">{escape(q.lot_id.name or "")}</td>
                    </tr>'''
                rec.adjustment_preview = f'''
                    <table style="width:100%; border-collapse:collapse; font-size:12px;">
                        <thead>
                            <tr style="background:#1F5C99; color:white;">
                                <th style="padding:5px 8px; text-align:left;">Producto</th>
                                <th style="padding:5px 8px; text-align:left;">Ubicación</th>
                                <th style="padding:5px 8px; text-align:right;">Sistema</th>
                                <th style="padding:5px 8px; text-align:right;">Contado</th>
                                <th style="padding:5px 8px; text-align:right;">Diferencia</th>
                                <th style="padding:5px 8px; text-align:left;">Lote/Serie</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                ''' if rows else '<p>Sin diferencias detectadas.</p>'
            except Exception:
                rec.adjustment_preview = '<p>Error al cargar vista previa.</p>'

    def action_submit(self):
        """Crea la solicitud de ajuste y notifica al aprobador."""
        self.ensure_one()

        if not self.reason or not self.reason.strip():
            raise UserError(_('Debes ingresar el motivo del ajuste.'))

        ids = json.loads(self.quant_ids_context or '[]')
        quants = self.env['stock.quant'].browse(ids)

        if not quants:
            raise UserError(_('No se encontraron productos para ajustar.'))

        # Serializar el snapshot del ajuste
        lines = []
        quant_snapshot = []
        for q in quants:
            lines.append({
                'product': q.product_id.display_name,
                'location': q.location_id.complete_name,
                'qty_system': q.quantity,
                'qty_counted': q.inventory_quantity,
                'diff': q.inventory_diff_quantity,
                'lot': q.lot_id.name if q.lot_id else '',
            })
            quant_snapshot.append({
                'id': q.id,
                'inventory_quantity': q.inventory_quantity,
            })

        # Buscar aprobador (grupo aprobador - primer usuario activo)
        approver_group = self.env.ref(
            'almx_stock_adjustment_approval.group_stock_adjustment_approver'
        )
        approvers = approver_group.user_ids.filtered(lambda u: u.active)
        if not approvers:
            raise UserError(_(
                'No hay ningún aprobador configurado. '
                'Contacta al administrador de TI (Irving).'
            ))
        # Usar Hamdi como aprobador principal (ID 12), o el primero disponible
        approver = approvers.filtered(lambda u: u.id == 12) or approvers[0]

        # Crear la solicitud
        request = self.env['stock.adjustment.request'].sudo().create({
            'requester_id': self.env.user.id,
            'reason': self.reason.strip(),
            'adjustment_lines_json': json.dumps(lines),
            'quant_ids_json': json.dumps(quant_snapshot),
        })

        # Crear actividad para el aprobador
        activity_type = self.env['mail.activity.type'].search(
            [('res_model', '=', False)], limit=1
        ) or self.env['mail.activity.type'].browse(2)

        self.env['mail.activity'].sudo().create({
            'activity_type_id': activity_type.id,
            'res_model_id': self.env['ir.model']._get('stock.adjustment.request').id,
            'res_id': request.id,
            'user_id': approver.id,
            'summary': _('⚠️ Aprobar Ajuste de Inventario - %s') % self.env.user.name,
            'note': _(
                '<p>El usuario <strong>%s</strong> solicita un ajuste de inventario.</p>'
                '<p><strong>Motivo:</strong> %s</p>'
                '<p>Haz clic en la solicitud para revisar el detalle y Aprobar o Rechazar.</p>'
            ) % (self.env.user.name, self.reason.strip()),
            'date_deadline': fields.Date.today(),
        })

        # Post en el chatter de la solicitud
        request.message_post(
            body=_('Solicitud enviada por %s. Motivo: %s') % (
                self.env.user.name, self.reason.strip()
            )
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Solicitud Enviada'),
                'message': _(
                    'Tu solicitud %s fue enviada a %s para aprobación. '
                    'Recibirás una notificación con el resultado.'
                ) % (request.name, approver.name),
                'type': 'success',
                'sticky': True,
                'next': {'type': 'ir.actions.act_window_close'},
            },
        }
