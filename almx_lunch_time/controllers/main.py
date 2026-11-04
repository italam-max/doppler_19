# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, http
from odoo.exceptions import UserError
from odoo.http import request
from odoo.service.common import exp_version
from odoo.tools import py_to_js_locale

from odoo.addons.hr_attendance.controllers.main import HrAttendance

LUNCH_ACTIONS = ('lunch_start', 'lunch_end', 'check_out')


class HrAttendanceLunch(HrAttendance):

    @http.route('/almx_lunch_time/kiosk_app', type='http', auth='user')
    def kiosk_app(self):
        """Kiosko dentro de la app móvil. A diferencia de la ruta estándar, no cierra
        la sesión: la app la necesita para seguir abierta alrededor del kiosko."""
        if not request.env.user.has_group('hr_attendance.group_hr_attendance_user'):
            return request.not_found()
        company = request.env.company.sudo()
        departments = request.env['hr.department'].with_context(
            allowed_company_ids=[company.id],
        ).sudo().search_read(
            domain=[('company_id', '=', company.id)],
            fields=['id', 'name', 'total_employee'],
        )
        return request.render('hr_attendance.public_kiosk_mode', {
            'kiosk_backend_info': {
                'token': company.attendance_kiosk_key,
                'company_id': company.id,
                'company_name': company.name,
                'departments': [
                    {'id': dep['id'], 'name': dep['name'], 'count': dep['total_employee']}
                    for dep in departments
                ],
                'kiosk_mode': company.attendance_kiosk_mode,
                'from_trial_mode': False,
                'barcode_source': company.attendance_barcode_source,
                'device_tracking_enabled': company.attendance_device_tracking,
                'lang': py_to_js_locale(company.partner_id.lang or company.env.lang),
                'server_version_info': exp_version().get('server_version_info'),
            },
        })

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
