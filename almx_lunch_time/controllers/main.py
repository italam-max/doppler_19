# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, http
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.hr_attendance.controllers.main import HrAttendance

LUNCH_ACTIONS = ('lunch_start', 'lunch_end', 'check_out')


class HrAttendanceLunch(HrAttendance):

    @http.route()
    def employees_infos(self, token, limit, offset, domain):
        """La lista del kiosko solo distingue "presente/ausente": quien está en
        su almuerzo o ya regresó de él sigue estando en el sitio."""
        result = super().employees_infos(token, limit, offset, domain)
        if isinstance(result, dict):
            for record in result.get('records', []):
                if record.get('status') in ('lunch_start', 'lunch_end'):
                    record['status'] = 'checked_in'
        return result

    @http.route('/almx_lunch_time/employee_by_barcode', type='jsonrpc', auth='public')
    def employee_by_barcode(self, token, barcode):
        """Identifica al empleado por su gafete sin registrar ninguna acción."""
        company = self._get_company(token)
        if company:
            employee = request.env['hr.employee'].sudo().search(
                [('barcode', '=', barcode), ('company_id', '=', company.id)], limit=1)
            if employee:
                return self._get_employee_info_response(employee)
        return {}

    @http.route('/almx_lunch_time/kiosk_action', type='jsonrpc', auth='public')
    def kiosk_lunch_action(self, token, action, employee_id=False, pin_code=False,
                           barcode=False, latitude=False, longitude=False):
        """Registra almuerzo (inicio/fin) o salida desde el kiosko."""
        if action not in LUNCH_ACTIONS:
            return {}
        company = self._get_company(token)
        if not company:
            return {}

        employees = request.env['hr.employee'].sudo()
        if barcode:
            employee = employees.search(
                [('barcode', '=', barcode), ('company_id', '=', company.id)], limit=1)
        else:
            employee = employees.browse(employee_id).exists() if employee_id else employees
            if employee and (
                employee.company_id != company
                or (company.attendance_kiosk_use_pin and employee.pin != pin_code)
            ):
                employee = employees.browse()
        if not employee:
            return {}

        geo_information = None
        if action == 'check_out':
            geo_information = self._get_geoip_response(
                'kiosk', latitude=latitude, longitude=longitude,
                device_tracking_enabled=company.attendance_device_tracking)
        employee.with_context(attendance_action=action)._attendance_action_change(geo_information)

        response = self._get_employee_info_response(employee)
        if action in ('lunch_start', 'lunch_end'):
            attendance = employee.last_attendance_id
            response.update({
                'lunch_action': action,
                'lunch_time': attendance.lunch_start if action == 'lunch_start' else attendance.lunch_end,
            })
        return response

    @http.route('/almx_lunch_time/systray_action', type='jsonrpc', auth='user')
    def systray_lunch_action(self, action):
        """Inicio / fin de almuerzo desde el menú de asistencia del backend."""
        if action not in ('lunch_start', 'lunch_end'):
            raise UserError(_('Invalid attendance action.'))
        user = request.env.user
        get_company = getattr(self, '_get_active_company', None)
        if get_company:
            user = user.with_company(get_company(request))
        employee = user.employee_id
        if not employee:
            raise UserError(_('There is no employee linked to your user.'))
        employee.with_context(attendance_action=action)._attendance_action_change()
        return self._get_employee_info_response(employee)
