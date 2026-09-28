{
    'name': 'Alamex - Préstamo de Equipo de IT',
    'summary': 'Adjunta automáticamente las laptops y cargadores asignados al solicitante en las aprobaciones de préstamo de equipo',
    'description': """
Préstamo / resguardo de equipo de cómputo en Aprobaciones.

- Ubicación de stock de IT por empleado.
- Marcas de producto: Equipo de IT, Laptop, Cargador.
- Al crear una solicitud en una categoría marcada con "Adjuntar equipo de IT asignado",
  se llenan las líneas de equipo con las laptops y cargadores que existen en la
  ubicación de IT del solicitante (con su número de serie).
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Human Resources/Approvals',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['approvals', 'hr', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/approval_category_data.xml',
        'views/approval_category_views.xml',
        'views/approval_request_views.xml',
        'views/product_views.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': False,
}
