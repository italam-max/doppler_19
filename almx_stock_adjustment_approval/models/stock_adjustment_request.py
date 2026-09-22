# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from markupsafe import Markup, escape
import json


class StockAdjustmentRequest(models.Model):
    _name = 'stock.adjustment.request'
    _description = 'Solicitud de Ajuste de Inventario'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Referencia', required=True, copy=False,
        readonly=True, default=lambda self: _('Nuevo'),
    )
    state = fields.Selection([
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='pending', tracking=True, readonly=True)

    requester_id = fields.Many2one('res.users', string='Solicitante', required=True, readonly=True, tracking=True)
    approver_id = fields.Many2one('res.users', string='Aprobador', readonly=True, tracking=True)
    reason = fields.Text(string='Motivo del Ajuste', required=True, readonly=True)
    rejection_reason = fields.Text(string='Motivo de Rechazo', readonly=True)
    date_request = fields.Datetime(string='Fecha de Solicitud', default=fields.Datetime.now, readonly=True)
    date_resolved = fields.Datetime(string='Fecha de Resolución', readonly=True)
    adjustment_lines_json = fields.Text(string='Detalle del Ajuste (JSON)', readonly=True)
    adjustment_lines_display = fields.Html(
        string='Detalle del Ajuste',
        compute='_compute_adjustment_lines_display',
        sanitize=False,
    )
    quant_ids_json = fields.Text(string='IDs de Quants', readonly=True)

    @api.depends('adjustment_lines_json')
    def _compute_adjustment_lines_display(self):
        for rec in self:
            if not rec.adjustment_lines_json:
                rec.adjustment_lines_display = '<p>Sin detalle.</p>'
                continue
            try:
                lines = json.loads(rec.adjustment_lines_json)
                rows = ''.join(
                    f'<tr>'
                    f'<td style="padding:4px 8px;">{escape(l.get("product",""))}</td>'
                    f'<td style="padding:4px 8px;">{escape(l.get("location",""))}</td>'
                    f'<td style="padding:4px 8px; text-align:right;">{l.get("qty_system",0):.2f}</td>'
                    f'<td style="padding:4px 8px; text-align:right;">{l.get("qty_counted",0):.2f}</td>'
                    f'<td style="padding:4px 8px; text-align:right; color:{"red" if l.get("diff",0) < 0 else "green"};">{l.get("diff",0):+.2f}</td>'
                    f'<td style="padding:4px 8px;">{escape(l.get("lot",""))}</td>'
                    f'</tr>'
                    for l in lines
                )
                rec.adjustment_lines_display = (
                    '<table style="width:100%;border-collapse:collapse;font-size:13px;">'
                    '<thead><tr style="background:#1F5C99;color:white;">'
                    '<th style="padding:6px 8px;text-align:left;">Producto</th>'
                    '<th style="padding:6px 8px;text-align:left;">Ubicación</th>'
                    '<th style="padding:6px 8px;text-align:right;">En Sistema</th>'
                    '<th style="padding:6px 8px;text-align:right;">Contado</th>'
                    '<th style="padding:6px 8px;text-align:right;">Diferencia</th>'
                    '<th style="padding:6px 8px;text-align:left;">Lote/Serie</th>'
                    '</tr></thead>'
                    f'<tbody>{rows}</tbody></table>'
                )
            except Exception:
                rec.adjustment_lines_display = '<p>Error al mostrar detalle.</p>'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code('stock.adjustment.request') or _('Nuevo')
        return super().create(vals_list)

    def action_approve(self):
        self.ensure_one()
        if self.state != 'pending':
            raise UserError(_('Esta solicitud ya fue procesada.'))

        if not self.env.user.has_group('almx_stock_adjustment_approval.group_stock_adjustment_approver'):
            raise UserError(_('Solo el aprobador autorizado puede aprobar ajustes.'))

        if self.quant_ids_json:
            try:
                quant_data = json.loads(self.quant_ids_json)
                for item in quant_data:
                    quant = self.env['stock.quant'].browse(item['id'])
                    if quant.exists():
                        quant.sudo().write({
                            'inventory_quantity': item['inventory_quantity'],
                            'inventory_quantity_set': True,
                        })
                quants = self.env['stock.quant'].browse([item['id'] for item in quant_data])
                quants.sudo().with_context(bypass_adjustment_approval=True).action_apply_inventory()
            except Exception as e:
                raise UserError(_(
                    'Error al aplicar el ajuste: %s\n\n'
                    'Puedes aplicarlo manualmente desde Inventario → Ajuste Físico.'
                ) % str(e))

        self.write({
            'state': 'approved',
            'approver_id': self.env.user.id,
            'date_resolved': fields.Datetime.now(),
        })

        # Notificar en el chatter mencionando al solicitante
        self.sudo().message_post(
            body=Markup(_(
                '<p>✅ <strong>Ajuste aprobado y aplicado</strong> por %s.</p>'
                '<p>%s tu solicitud fue aprobada y el ajuste de inventario ha sido aplicado.</p>'
            )) % (self.env.user.name, self.requester_id.name),
            partner_ids=[self.requester_id.partner_id.id],
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Ajuste Aprobado'),
                'message': _('El ajuste de inventario ha sido aprobado y aplicado correctamente.'),
                'type': 'success',
                'sticky': False,
            },
        }

    def action_reject(self):
        self.ensure_one()
        if self.state != 'pending':
            raise UserError(_('Esta solicitud ya fue procesada.'))

        if not self.env.user.has_group('almx_stock_adjustment_approval.group_stock_adjustment_approver'):
            raise UserError(_('Solo el aprobador autorizado puede rechazar ajustes.'))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Motivo de Rechazo'),
            'res_model': 'stock.adjustment.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_request_id': self.id},
        }

    def _notify_requester(self, approved=True, rejection_reason=''):
        """
        Notifica al solicitante mediante message_post en el chatter
        de la solicitud, mencionándolo para que reciba notificación interna.
        Evita crear mail.activity que en Odoo Enterprise con documents
        intenta hacer action_notify sobre res.users (sin mail.thread).
        """
        if approved:
            body = Markup(_(
                '<p>✅ <strong>Solicitud Aprobada</strong></p>'
                '<p>Tu solicitud <strong>%s</strong> fue aprobada y aplicada por <strong>%s</strong>.</p>'
            )) % (self.name, self.approver_id.name or 'el aprobador')
        else:
            body = Markup(_(
                '<p>❌ <strong>Solicitud Rechazada</strong></p>'
                '<p>Tu solicitud <strong>%s</strong> fue rechazada.</p>'
                '<p><strong>Motivo:</strong> %s</p>'
                '<p>Si tienes dudas, contacta a tu supervisor.</p>'
            )) % (self.name, rejection_reason or 'Sin motivo especificado')

        self.sudo().message_post(
            body=body,
            partner_ids=[self.requester_id.partner_id.id],
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
