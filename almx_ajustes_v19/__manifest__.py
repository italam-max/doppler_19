{
    'name': 'Alamex - Ajustes de migración 16 → 19',
    'version': '19.0.1.0.0',
    'summary': 'Recupera en Odoo 19 la funcionalidad de 16 que se perdió en la migración',
    'description': """
Ajustes detectados en la validación por áreas (oct 2026):

* Aprobaciones: Responsable, estado "Hecho" y grupos de lectura por categoría
  (antes en el módulo doppler de Vauxoo).
* Tiempo personal: doble aprobación obligatoria en dos pasos, respaldo de RH,
  sin autoaprobación y tipos restringidos para empleados.
* Soporte: cada usuario ve solo sus tickets; grupo para ver todas las mesas.
* Proyectos: secciones Fechas y estatus y Documentos de la tarea (almx_project).
* Reclutamiento: método de la plantilla Job Offer y formulario de postulación.
* Empleados: fechas de ingreso / salida / motivo y datos SAT-IMSS de consulta.
    """,
    'author': 'Doppler Elevadores - Área TDI',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'depends': [
        'hr',
        'project',
        'approvals',
        'hr_holidays',
        'helpdesk',
        'lunch',
        'hr_recruitment',
        'website_hr_recruitment',
        'almx_employee',
    ],
    'data': [
        'security/groups.xml',
        'security/rules.xml',
        'views/approval_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_employee_views.xml',
        'views/project_task_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
