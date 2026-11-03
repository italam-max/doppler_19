# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Alamex: Tiempo de comida',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Attendances',
    'author': 'Dev JS',
    'sequence': 99,
    'summary': 'Lunch Start Time And End Time  Hr Attendance',
    'depends': [
        'hr',
        'hr_attendance',
    ],
    'data': [
        'views/hr_attendance.xml',
    ],
    'assets': {
        # Systray (menú de asistencia dentro del backend)
        'web.assets_backend': [
            'almx_lunch_time/static/src/systray/**/*',
        ],
        # Kiosko público de asistencias (bundle propio de hr_attendance)
        'hr_attendance.assets_public_attendance': [
            'almx_lunch_time/static/src/public_kiosk/**/*',
        ],
    },
    'demo': [],
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 15,
    'currency': 'EUR',
    'license': 'LGPL-3',
}
