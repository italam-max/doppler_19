{
    'name': 'Catálogo de productos (Alamex)',
    'version': '19.0.1.0.0',
    'summary': 'Consulta de productos de solo lectura: nombre, SKU, código de barras y categoría, sin precios ni existencias',
    'category': 'Inventory/Inventory',
    'author': 'Alamex - TDI',
    'depends': ['product'],
    'data': [
        'security/security.xml',
        'views/product_catalog_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
