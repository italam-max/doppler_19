{
    'name': 'Alamex - Métodos de envío',
    'version': '19.0.1.4.0',
    'summary': 'Métodos de envío, dirección de entrega y datos fiscales capturados por ventanas desde la venta',
    'author': 'Alamex',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['sale_stock', 'stock_delivery', 'l10n_mx_edi', 'almx_sale', 'almx_stock', 'almx_csf'],
    'data': [
        'security/ir.model.access.csv',
        'data/delivery_carrier_data.xml',
        'wizard/shipping_wizard_views.xml',
        'views/delivery_carrier_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'almx_metodo_envio/static/src/js/carrier_wizard_field.js',
        ],
    },
    'installable': True,
    'application': False,
}
