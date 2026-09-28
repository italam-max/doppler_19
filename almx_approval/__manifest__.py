{
    'name': 'Alamex - Aprobaciones',
    'summary': 'Campos de pago, OC y gastos en solicitudes de aprobación',
    'description': """
Ajustes de Alamex sobre Aprobaciones:

- Moneda, motivo de urgencia y "¿Tengo una PO?" (campos de Studio) en el formulario.
- OC ligada a la solicitud (obligatoria si se marca "¿Tengo una PO?").
- Gastos ligados a la solicitud (en 19 ya no existe el Informe de gastos).
- "Pagado" solo editable por Contabilidad / Administrador.
- Aprobadores de solo lectura en la solicitud (se definen en la categoría).
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Human Resources/Approvals',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['approvals', 'purchase', 'hr_expense'],
    'data': [
        'views/approval_request_views.xml',
    ],
    'installable': True,
    'application': False,
}
