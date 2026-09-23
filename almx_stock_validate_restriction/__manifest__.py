{
    'name': 'ALMX - Restricción de Validación de Transferencias',
    'version': '19.0.1.4.0',
    'summary': 'Bloquea OUT sin PICK terminado + candado anti-negativos + semáforo visual',
    'description': """
        Portado de stock_validate_restriction (16.0.1.3.1) a Odoo 19.

        1. Consistencia PICK -> OUT: no se puede validar una salida por más
           cantidad de la que realmente se recolectó en su paso previo.
        2. Candado anti-negativos: antes de validar cualquier PICK, OUT o
           traslado interno desde ubicación interna, recorta la cantidad al
           físico real (menos lo reservado por otros). El faltante queda en
           backorder nativo en vez de generar stock negativo.
        3. Encadenamiento: al validar el PICK, si la OUT relacionada queda
           disponible, se valida automáticamente.
        4. Semáforo verde/rojo en las líneas de operación.

        Cambios respecto a 16:
        - qty_done / reserved_uom_qty / quantity_done -> quantity + picked.
        - Solo se evalúan los movimientos que Odoo realmente va a procesar
          (si hay movimientos marcados como "picked", solo esos).
        - Cantidades en UdM del producto antes de comparar contra quants.
        - PICK->OUT descuenta lo que ya salió en OUTs previas (backorders)
          del mismo PICK.
        - Encadenamiento usa products_availability_state (no el texto
          traducido) y corre en savepoint: si la OUT no se puede validar,
          el PICK sí queda validado y se deja nota en la OUT.
        - Semáforo evalúa el movimiento completo, no cada línea contra toda
          la demanda (evita rojo falso con varios lotes).
    """,
    'author': 'Irving Sammer González Correa - Alamex',
    'category': 'Inventory/Inventory',
    'depends': ['stock', 'almx_stock_extends'],
    'data': [
        'views/stock_move_line_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
