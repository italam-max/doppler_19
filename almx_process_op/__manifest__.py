{
    'name': 'Alamex - Seguimiento de Proceso Operaciones',
    'summary': 'Finanzas marca si una solicitud de aprobación siguió o no el proceso',
    'description': """
Seguimiento de proceso de Finanzas hacia Operaciones en Aprobaciones:

- "Solicitud dentro del proceso" / "Solicitud fuera del proceso" (excluyentes).
- Motivo obligatorio cuando la solicitud salió de proceso.
- Solo visible para el grupo "Seguimiento de Proceso OP". Cambios con seguimiento en el chatter.
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Human Resources/Approvals',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['approvals'],
    'data': [
        'security/groups.xml',
        'views/approval_request_views.xml',
    ],
    'installable': True,
    'application': False,
}
