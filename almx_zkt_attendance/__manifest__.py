{
    'name': 'Alamex - Checador ZKTeco (ADMS Push)',
    'version': '19.0.1.4.0',
    'category': 'Human Resources/Attendances',
    'summary': 'Integración en tiempo real de terminales ZKTeco (protocolo ADMS/push) con Asistencias (hr.attendance)',
    'description': """
Checador ZKTeco - Integración ADMS
===================================

Recibe los checadas (checkin/checkout) que empuja en tiempo real una terminal
ZKTeco (ej. F22) configurada en modo "Cloud Server / ADMS", y las convierte
automáticamente en registros de hr.attendance.

No requiere IP pública ni acceso entrante hacia la terminal: el equipo es
quien se conecta hacia Odoo por HTTPS, por lo que funciona aunque la terminal
esté en una red local sin salida directa configurada de antemano (solo
necesita internet saliente).

Componentes:
- zk.device: catálogo de terminales autorizadas (número de serie, zona horaria).
- hr.employee.zk_pin: número de enrolamiento (PIN) del empleado en el equipo.
- Endpoints /iclock/cdata, /iclock/getrequest, /iclock/devicecmd (protocolo ADMS).
""",
    'author': 'Alamex',
    'depends': ['hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/zk_device_views.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
