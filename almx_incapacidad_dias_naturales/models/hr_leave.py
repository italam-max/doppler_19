import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    is_incapacidad = fields.Boolean(
        string='Contar días naturales (Incapacidad)',
        help='Las ausencias de este tipo cuentan días naturales (incluye sábados, '
             'domingos y festivos) en lugar de los días laborables del empleado.')


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # En 19 la duración se calcula en _get_durations(); _get_number_of_days() ya no existe.
    def _get_durations(self, check_leave_type=True, resource_calendar=None):
        result = super()._get_durations(check_leave_type=check_leave_type, resource_calendar=resource_calendar)
        for leave in self:
            if not (leave.holiday_status_id.is_incapacidad and leave.request_date_from and leave.request_date_to):
                continue
            days = (leave.request_date_to - leave.request_date_from).days + 1
            calendar = (resource_calendar or leave.resource_calendar_id
                        or leave.employee_id.resource_calendar_id or leave.company_id.resource_calendar_id)
            hours = days * (calendar.hours_per_day or 8.0)
            result[leave.id] = (days, hours)
        return result
