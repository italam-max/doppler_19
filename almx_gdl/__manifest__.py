# -*- coding: utf-8 -*-
{
    'name': 'ALMX - Venta desde GDL / Almacén de Retirada',
    'version': '19.0.1.1.0',
    'summary': 'Almacén de Retirada por línea de venta (Almacén 2, Almacén 3 o GDL) '
               'limitado a ubicaciones con existencia y al grupo Acceso Multi-Almacén GDL',
    'description': """
Validación de stock multi-almacén en Ventas (GDL / CDMX)
==========================================================

Qué hace
--------
1. Campos NO almacenados en sale.order.line con la existencia disponible en
   Almacén 2, Almacén 3 (CDMX) y GDL/Existencias, calculada al momento.
2. "Almacén de Retirada" por línea: solo deja elegir entre las ubicaciones
   con existencia real del producto. Al elegir GDL se agrega la ruta de GDL
   (entrega en 1 paso) y la línea se surte desde el almacén de GDL; al elegir
   Almacén 2/3 se quita esa ruta y sigue el flujo default de CDMX (PICK+OUT).
   No dispara traslados ni reabastos automáticos.
3. Solo el grupo "Acceso Multi-Almacén GDL" ve y edita Almacén de Retirada y
   las rutas de la línea. Respaldo server-side: no se puede guardar una
   ubicación sin existencia (ni por RPC).

Parámetros (Ajustes técnicos > Parámetros del sistema), opcionales:
- sale_multi_warehouse_validation.location_alm2_id (default 1519)
- sale_multi_warehouse_validation.location_alm3_id (default 1520)
- sale_multi_warehouse_validation.location_gdl_id  (default 3600)
- sale_multi_warehouse_validation.route_gdl_id     (default 131)

Changelog
---------
- 19.0.1.1.0: Port a Odoo 19.
  - route_id (Many2one) -> route_ids (Many2many) en la línea de venta. Al
    elegir Almacén 2/3 solo se quita la ruta de GDL (no se borran otras
    rutas que la línea pudiera tener).
  - Se elimina el override de _prepare_procurement_values que forzaba
    warehouse_id=GDL: en 19 sale_stock calcula warehouse_id de la línea a
    partir de las reglas de su ruta, así que con la ruta de GDL ya queda en
    el almacén correcto de forma nativa.
  - El grupo se declara en este módulo (almx_gdl.group_acceso_multialmacen_gdl).
    Un pre_init_hook reasigna el xmlid hecho a mano en 16
    (doppler_custom.group_acceso_multialmacen_gdl) para conservar el mismo
    grupo (id 603) y sus miembros.
  - type == 'product' -> is_storable; precisión 'Product Unit'; tree -> list.
- 16.0.1.0.0: Versión inicial.
""",
    'author': 'Irving Sammer González Correa - Alamex',
    'category': 'Sales/Inventory',
    'depends': ['sale_stock', 'stock'],
    'data': [
        'security/security.xml',
        'views/sale_order_views.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
