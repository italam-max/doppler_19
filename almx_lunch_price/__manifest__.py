{
    'name': 'Almuerzo: precio editable en control de proveedores',
    'version': '19.0.1.1.1',
    'category': 'Human Resources/Lunch',
    'summary': 'Permite editar el precio en Almuerzo > Gerente > Control de proveedores '
               'solo a los usuarios del grupo "Editor de precios de almuerzo".',
    'author': 'Celia Hernandez',
    'website': "www.alam.mx",
    'license': 'LGPL-3',
    'depends': ['lunch'],
    'data': [
        'security/security.xml',
        'views/lunch_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'almx_lunch_price/static/src/views/*.js',
        ],
    },
    'installable': True,
    'application': False,
}
