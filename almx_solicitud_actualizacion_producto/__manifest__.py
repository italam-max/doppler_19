{
    'name': 'ALMX - Solicitud de Actualización de Producto',
    'version': '19.0.1.1.0',
    'summary': 'Botón para Compras que crea las actividades de actualización de ficha a cada área',
    'description': """
Desde la ficha del producto (solo grupo Compras) se solicita la actualización:
se crea una actividad por cada tarea configurada (SKU, fotografías, código SAT,
fichas técnicas, puntos de control de calidad) a su responsable, con su plazo.
Si el producto ya tiene el proceso en curso, no se duplica.

Las tareas y sus responsables se configuran en Compras > Configuración >
Tareas de actualización de producto (antes estaban fijas en el código).

Changelog
---------
- 19.0.1.1.0: Port a 19 (antes solicitud_actualizacion_producto 16.0.1.0.0).
  - Responsables, plazos y textos configurables (modelo almx.product.update.task)
    en lugar de ids de usuario fijos en el código.
  - Si una tarea no tiene responsable activo se avisa en el resultado en vez de
    omitirla en silencio.
  - Se quita la dependencia a quality_control (no se usaba).
- 16.0.1.0.0: Versión inicial.
""",
    'category': 'Inventory/Purchase',
    'author': 'Irving Sammer González Correa - Alamex',
    'depends': ['product', 'purchase', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/activity_type_data.xml',
        'data/task_data.xml',
        'data/server_action_data.xml',
        'views/product_update_task_views.xml',
        'views/product_template_views.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
