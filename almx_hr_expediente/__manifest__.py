{
    "name": "Alamex - Expediente digital RH",
    "version": "19.0.1.1.0",
    "summary": "Pestaña RRHH / Expediente en el empleado: documentos, psicometría e historial de contratos",
    "author": "Alamex - TDI",
    "license": "LGPL-3",
    "category": "Human Resources/Employees",
    "depends": ["hr", "hr_recruitment"],
    "data": [
        "security/groups.xml",
        "views/hr_version_views.xml",
        "views/hr_employee_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
