from markupsafe import Markup

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # El contexto viaja al selector de tipo para filtrar los tipos "Solo RH".
    holiday_status_id = fields.Many2one(context={'almx_restrict_leave_types': True})

    @api.model
    def default_get(self, fields):
        defaults = super().default_get(fields)
        leave_type_model = self.env['hr.leave.type']
        type_id = defaults.get('holiday_status_id')
        if type_id and not leave_type_model._almx_user_can_use_all_types():
            if leave_type_model.browse(type_id).almx_restricted:
                allowed = leave_type_model.search([
                    ('almx_restricted', '=', False),
                    '|', ('requires_allocation', '=', False), ('has_valid_allocation', '=', True),
                ], order='sequence', limit=1)
                defaults['holiday_status_id'] = allowed.id or False
                if allowed:
                    defaults['request_unit_hours'] = allowed.request_unit == 'hour'
        return defaults

    @api.constrains('holiday_status_id')
    def _almx_check_restricted_leave_type(self):
        if self.env['hr.leave.type']._almx_user_can_use_all_types():
            return
        for leave in self:
            if leave.holiday_status_id.almx_restricted:
                raise ValidationError(self.env._(
                    'El tipo "%s" solo lo puede registrar Recursos Humanos. '
                    'Solicita a RH que lo capture por ti.',
                    leave.holiday_status_id.display_name,
                ))

    def _get_next_states_by_state(self):
        """Reglas de Alamex sobre el flujo nativo de 19:

        * Doble aprobación ('both'): siempre en dos pasos. En 19 el encargado
          de RH puede pasar de "Por aprobar" a "Validado" en un clic; aquí se
          obliga a pasar primero por "Segunda aprobación".
        * Nadie aprueba ni valida su propia ausencia.
        """
        result = super()._get_next_states_by_state()
        if self.validation_type == 'both':
            for state in ('confirm', 'refuse', 'cancel'):
                result[state].discard('validate')
        if self.employee_id and self.employee_id in self.env.user.employee_ids:
            for targets in result.values():
                targets.discard('validate1')
                targets.discard('validate')
        return result

    def action_approve(self, check_state=True):
        # Primer paso dado por RH en lugar del jefe: queda registrado en el chatter.
        hr_first_step = self.filtered(
            lambda l: l.state == 'confirm'
            and l.validation_type == 'both'
            and l.employee_id.leave_manager_id
            and l.employee_id.leave_manager_id != self.env.user
        )
        result = super().action_approve(check_state=check_state)
        for leave in hr_first_step.filtered(lambda l: l.state == 'validate1'):
            leave.message_post(
                body=Markup('%s') % self.env._(
                    'Primer paso aprobado por %(rh)s (RH) en lugar del jefe '
                    'directo %(jefe)s.',
                    rh=self.env.user.name,
                    jefe=leave.employee_id.leave_manager_id.name,
                ),
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )
        return result
