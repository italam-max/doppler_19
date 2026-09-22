# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockAdjustmentRejectWizard(models.TransientModel):
    _name = 'stock.adjustment.reject.wizard'
    _description = 'Wizard - Rechazo de Ajuste de Inventario'

    request_id = fields.Many2one(
        'stock.adjustment.request',
        string='Solicitud',
        required=True,
        readonly=True,
    )
    rejection_reason = fields.Text(
        string='Motivo del Rechazo',
        required=True,
    )

    def action_confirm_reject(self):
        self.ensure_one()
        if not self.rejection_reason or not self.rejection_reason.strip():
            raise UserError(_('Debes ingresar el motivo del rechazo.'))

        request = self.request_id
        request.write({
            'state': 'rejected',
            'approver_id': self.env.user.id,
            'rejection_reason': self.rejection_reason.strip(),
            'date_resolved': fields.Datetime.now(),
        })
        request.message_post(
            body=_('❌ Solicitud rechazada por %s. Motivo: %s') % (
                self.env.user.name, self.rejection_reason.strip()
            )
        )

        # Notificar al solicitante
        request._notify_requester(
            approved=False,
            rejection_reason=self.rejection_reason.strip(),
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Solicitud Rechazada'),
                'message': _('La solicitud fue rechazada y el solicitante fue notificado.'),
                'type': 'warning',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            },
        }
