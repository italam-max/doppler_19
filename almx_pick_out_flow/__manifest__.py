{
    'name': 'ALMX - Flujo PICK → OUT',
    'version': '19.0.1.2.0',
    'summary': 'URLs en el PICK, OUT con botón Crear OUT y Comprobante obligatorio al validar el OUT',
    'description': """
Cambio PICK antes de OUT (WHTL):
- URL Almacén / URL Bodega / URL Laboratorio / URL Calidad se capturan en el PICK
  y se reflejan en el OUT ligado en solo lectura (si el PICK no trae valor, el OUT
  sigue editable).
- Validar el PICK ya no genera el OUT: lo crea el botón "Crear OUT", solo en PICK
  validado sin OUT y solo para el grupo "Alamex: Crear OUT manual (traslados)".
  Con la ruta nativa de 19 (venta → PICK con destino final Clientes + regla push
  Almacén 1 → Clientes) el OUT conserva la línea de venta y el encadenamiento.
- Comprobante (x_studio_comprobante): se puede subir antes de validar el OUT; si no
  está, al validar se pide (PDF o foto). Sin Comprobante no se valida.
""",
    'author': 'Doppler Elevadores - TDI',
    'category': 'Inventory/Inventory',
    'license': 'LGPL-3',
    'depends': ['stock', 'sale_stock', 'almx_stock', 'almx_stock_extends'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/comprobante_wizard_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_picking_create_out_views.xml',
        'views/stock_picking_type_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
