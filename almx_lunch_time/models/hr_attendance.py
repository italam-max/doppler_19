# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

LUNCH_ACTIONS = ('lunch_start', 'lunch_end', 'check_out')


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    lunch_start = fields.Datetime('Lunch Start Time')
    lunch_end = fields.Datetime('Lunch End Time')

    @api.constrains('check_in', 'check_out', 'lunch_start', 'lunch_end')
    def _check_lunch_times(self):
        for attendance in self:
            if attendance.lunch_end and not attendance.lunch_start:
                raise ValidationError(_('"Lunch End" cannot be set without a "Lunch Start".'))
            if attendance.lunch_start and attendance.check_in and attendance.lunch_start < attendance.check_in:
                raise ValidationError(_('"Lunch Start" cannot be earlier than "Check In".'))
            if attendance.lunch_start and attendance.lunch_end and attendance.lunch_end < attendance.lunch_start:
                raise ValidationError(_('"Lunch End" cannot be earlier than "Lunch Start".'))
            if attendance.check_out:
                if attendance.lunch_start and attendance.lunch_start > attendance.check_out:
                    raise ValidationError(_('"Lunch Start" cannot be later than "Check Out".'))
                if attendance.lunch_end and attendance.lunch_end > attendance.check_out:
                    raise ValidationError(_('"Lunch End" cannot be later than "Check Out".'))

    @api.depends('lunch_start', 'lunch_end')
    def _compute_worked_hours(self):
        super()._compute_worked_hours()
        # Si el empleado registró su almuerzo real (inicio y fin) se descuenta ese
        # tiempo en lugar del descanso teórico del calendario (no se resta dos veces).
        for attendance in self:
            if (attendance.check_in and attendance.check_out
                    and attendance.lunch_start and attendance.lunch_end
                    and attendance.lunch_end > attendance.lunch_start):
                total = (attendance.check_out - attendance.check_in).total_seconds()
                lunch_start = max(attendance.lunch_start, attendance.check_in)
                lunch_end = min(attendance.lunch_end, attendance.check_out)
                lunch = max((lunch_end - lunch_start).total_seconds(), 0.0)
                attendance.worked_hours = max(total - lunch, 0.0) / 3600.0


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_state = fields.Selection(selection_add=[
        ('lunch_start', 'Lunch Start'),
        ('lunch_end', 'Lunch End'),
    ])

    @api.depends(
        'last_attendance_id.check_in', 'last_attendance_id.check_out',
        'last_attendance_id.lunch_start', 'last_attendance_id.lunch_end',
        'last_attendance_id',
    )
    def _compute_attendance_state(self):
        for employee in self:
            att = employee.last_attendance_id.sudo()
            if not att or att.check_out:
                employee.attendance_state = 'checked_out'
            elif att.lunch_start and att.lunch_end:
                employee.attendance_state = 'lunch_end'
            elif att.lunch_start:
                employee.attendance_state = 'lunch_start'
            else:
                employee.attendance_state = 'checked_in'

    @api.depends('attendance_state')
    def _compute_presence_state(self):
        super()._compute_presence_state()
        # Quien ya regresó de comer está trabajando: se muestra como presente.
        for employee in self:
            if employee.sudo().attendance_state == 'lunch_end':
                employee.hr_presence_state = 'present'

    def _attendance_action_change(self, geo_information=None):
        """Check in / lunch start / lunch end / check out.

        La acción deseada llega en el contexto (``attendance_action``). Sin acción
        se conserva el comportamiento estándar: si está fuera hace check in y si
        está dentro hace check out.
        """
        self.ensure_one()
        state = self.attendance_state
        action = self.env.context.get('attendance_action')

        if action and action not in LUNCH_ACTIONS:
            raise UserError(_('Invalid attendance action.'))

        if state == 'checked_out':
            if action in ('lunch_start', 'lunch_end'):
                raise UserError(_('%(empl_name)s must check in before registering lunch.',
                                  empl_name=self.sudo().name))
            return super()._attendance_action_change(geo_information)

        action = action or 'check_out'
        attendance = self.env['hr.attendance'].search(
            [('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        if not attendance:
            raise UserError(_(
                'Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.',
                empl_name=self.sudo().name))

        action_date = fields.Datetime.now()
        if action == 'lunch_start':
            if state != 'checked_in':
                raise UserError(_('%(empl_name)s cannot start lunch right now.',
                                  empl_name=self.sudo().name))
            attendance.write({'lunch_start': action_date})
        elif action == 'lunch_end':
            if state != 'lunch_start':
                raise UserError(_('%(empl_name)s is not on lunch.',
                                  empl_name=self.sudo().name))
            attendance.write({'lunch_end': action_date})
        else:
            vals = {'check_out': action_date}
            if attendance.lunch_start and not attendance.lunch_end:
                # Salió sin marcar el regreso: se cierra el almuerzo con la salida.
                vals['lunch_end'] = action_date
            if geo_information:
                vals.update({'out_%s' % key: value for key, value in geo_information.items()})
            attendance.write(vals)
        return attendance
