{
    'name': 'ALMX - Candado Estricto de Productos',
    'version': '19.0.1.1.0',
    'category': 'Sales',
    'summary': 'Solo el grupo "Permitir Crear Productos" puede dar de alta productos o variantes.',
    'description': """
Bloquea la creación de productos en el sistema.

- Por defecto NADIE puede crear productos.
- Solo el grupo "Permitir Crear Productos" puede hacerlo (Dirección y TI).
- Aplica desde el formulario, importación, duplicado y RPC.

Changelog
---------
- 19.0.1.1.0: Port a 19 (antes strict_product_lock 16.0.1.0.1).
  - También bloquea crear variantes (product.product): en 16 se podía dar
    de alta una variante nueva agregando un valor de atributo o creando la
    variante directo, aunque la plantilla estuviera bloqueada.
  - Grupo sin categoría (en 19 res.groups ya no usa category_id).
- 16.0.1.0.1: Versión inicial.
""",
    'author': 'Irving Sammer González Correa - Alamex',
    'depends': ['product'],
    'data': ['security/groups.xml'],
    'pre_init_hook': 'pre_init_hook',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
