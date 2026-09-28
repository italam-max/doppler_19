{
    'name': 'Alamex - Empleados y Expediente',
    'version': '19.0.1.0.0',
    'summary': 'Documentos del empleado, candidato de origen y expediente de eventos (reemplaza el modelo Studio x_hr.employee.file)',
    'description': """
- Muestra en el empleado los campos Studio de 16: fecha de ingreso, acuerdos firmados
  (descripción de puesto, uso de imagen, confidencialidad) y comprobantes IMSS/INFONAVIT/FONACOT.
- Candidato de origen (hr.applicant).
- Expediente del empleado: eventos de RH (onboarding, capacitación, actas, sanciones,
  reconocimientos, préstamos, etc.) con fecha, descripción y archivo. Solo RH.
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Human Resources/Employees',
    'depends': ['hr', 'hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'views/almx_employee_file_views.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
