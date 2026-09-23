{
    'name': 'ALMX - Compras: número de pedimento en importaciones',
    'version': '19.0.1.1.0',
    'summary': 'Pedimento obligatorio y con formato validado solo en recepciones de compras de importación',
    'description': """
Número de pedimento en recepciones (IN) de compras de importación
================================================================

- Proveedor: casilla "Proveedor de importación".
- Orden de compra: casilla "Importación" (toma el valor del proveedor y se
  puede ajustar por orden, p. ej. un proveedor nacional que factura un
  producto importado).
- Recepción ligada a una compra de importación: el número de pedimento es
  obligatorio para validar y debe tener el formato oficial de 15 dígitos
  (año 2, aduana 2, patente 4, número 7). Se guarda normalizado:
  "26 43 1925 6000244".
- Compras nacionales: el campo no aparece ni se exige.
- El pedimento solo se permite en entradas ligadas a una orden de compra.
- Registro de cambios en el chatter.

Changelog
---------
- 19.0.1.1.0: Port a 19 (Celia Hernández, 16).
  - En 16 era obligatorio en TODA recepción de compra, incluidas nacionales,
    que no tienen pedimento: de 204 capturas solo 113 eran pedimentos; el
    resto era relleno ("N/A", "0", números de PO, notas, contenedores).
    Ahora solo se exige en importaciones y se valida el formato.
  - Como la mayoría de proveedores extranjeros no tienen país capturado, la
    regla usa la casilla del proveedor/orden en lugar del país. Al instalar
    se marcan los proveedores con país distinto a México.
  - Se quita el esqueleto sin uso (controllers, demo, vistas vacías y un
    permiso a un modelo inexistente).
- 16: Versión inicial.
""",
    'author': 'Celia Hernández / Irving Sammer González Correa - Alamex',
    'category': 'Inventory/Purchase',
    'depends': ['stock', 'purchase', 'purchase_stock'],
    'data': [
        'views/partner_views.xml',
        'views/purchase_views.xml',
        'views/stock_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
