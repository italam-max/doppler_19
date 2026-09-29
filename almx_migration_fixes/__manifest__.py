{
    'name': 'Alamex - Correcciones post-migración 16 → 19',
    'version': '19.0.1.0.0',
    'summary': 'Corrige restos del upgrade que hacen tronar menús: vistas inexistentes, íconos y permisos de reportes',
    'description': """
Se ejecuta al instalar y en cada actualización del módulo (idempotente):

1. Acciones de ventana con tipos de vista que en 19 no existen para su modelo
   (gantt, cohort, calendar, map, grid): se quitan del view_mode. Sin esto el menú
   truena con "Campos insuficientes para la vista de Gantt" o "No se encontró
   ninguna vista predeterminada de tipo cohort".
2. Menús raíz sin imagen de ícono (salen con la caja genérica): se regenera.
3. Permisos de lectura de los reportes de Compras e Inventario para los grupos
   "Report - Compras" y "Report - Inventario" (en 16 existían; el upgrade los perdió).

Pensado para correr también después de la migración final.
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Hidden',
    'depends': ['web', 'purchase', 'stock'],
    'data': [
        'data/fixes.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
