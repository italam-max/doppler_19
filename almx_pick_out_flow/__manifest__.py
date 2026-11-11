{
    'name': 'ALMX - Flujo PICK → OUT',
    'version': '19.0.1.0.0',
    'summary': 'URLs de surtido en el PICK, reflejadas en el OUT',
    'description': """
Fase 1 del cambio PICK antes de OUT (WHTL):
- URL Almacén / URL Bodega / URL Laboratorio se capturan en el PICK y se reflejan
  en el OUT ligado en solo lectura (transición: si el PICK no trae valor, el OUT
  sigue editable).
""",
    'author': 'Doppler Elevadores - TDI',
    'category': 'Inventory/Inventory',
    'license': 'LGPL-3',
    'depends': ['stock', 'almx_stock', 'almx_stock_extends'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}
