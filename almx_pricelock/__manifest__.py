# -*- coding: utf-8 -*-
{
    'name': 'ALMX - Candado y registro de precios de venta (producto y variante)',
    'version': '19.0.2.0.1',
    'summary': 'Solo el grupo "Editar precio de venta" cambia precios; precio independiente '
               'por variante; todo cambio queda registrado en el chatter',
    'description': """
Precio de venta: candado, registro y precio independiente por variante
======================================================================

1. Grupo "Editar precio de venta": solo sus miembros pueden cambiar el precio
   de venta del producto (plantilla) y el de cada variante. Aplica también por
   importación/RPC.
2. Registro: cada cambio de precio (plantilla o variante) queda en el chatter
   con usuario, fecha, valor anterior y nuevo.
3. Precio por variante: cada variante puede tener su propio precio de venta,
   independiente del precio base de la plantilla y de las demás variantes.
   En 0 = usa el cálculo nativo (precio base + extras de atributos).
   El precio de variante se usa en el cálculo de listas de precios (y por lo
   tanto en pedidos de venta), no solo en la ficha.

Changelog
---------
- 19.0.2.0.0: Port a 19 y consolidación con almx_variant_price (16.0.1), que
  deja de existir como módulo aparte.
  - En 16 el precio de variante (variant_price) no tenía candado ni registro:
    la vista lo escribía directo y no pasaba por el bloqueo de almx_pricelock.
    Ahora ambos precios están protegidos por el mismo grupo y con seguimiento.
  - En 16 el precio de variante solo cambiaba lo que se veía en la ficha: las
    listas de precios (y los pedidos de venta) seguían usando precio base +
    extras. Ahora _price_compute usa el precio de variante cuando existe.
  - Se quita el esqueleto sin uso (controllers, demo, templates, vistas
    vacías, ir.model.access de un modelo inexistente).
  - res.groups sin categoría (en 19 ya no existe category_id en grupos).
- 16.0.1: Versión inicial (Celia Hernández). Precio por variante:
  almx_variant_price 16.0.1 (Irving González).
""",
    'author': 'Celia Hernández / Irving Sammer González Correa - Alamex',
    'category': 'Sales/Sales',
    'depends': ['product', 'mail'],
    'data': [
        'security/security.xml',
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
