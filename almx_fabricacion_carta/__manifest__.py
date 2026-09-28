{
    'name': 'Alamex - Cartas de Fabricación (Instalaciones)',
    'version': '19.0.3.0.0',
    'summary': 'Genera y adjunta en el chatter las cartas MEX-OPE-ANX-07/08/09 al avanzar la tarea de etapa',
    'description': """
Al mover una tarea a una etapa configurada con carta (y viniendo de una de sus etapas de
origen), se genera el PDF correspondiente y se adjunta al chatter. Cada carta se genera
automáticamente una sola vez por tarea; después se reimprime desde Imprimir.

- MEX-OPE-ANX-07 Carta de Confirmación de Fabricación
- MEX-OPE-ANX-08 Carta de Confirmación de Término de Fabricación
- MEX-OPE-ANX-09 Carta de Notificación de Llegada de Equipo a Almacén

La configuración vive en la etapa (Proyecto > Configuración > Etapas), ya no en IDs fijos
duplicados en Python y JavaScript.
""",
    'author': 'Alamex / Doppler Elevadores (Irving Sammer González Correa)',
    'website': 'https://www.alam.mx',
    'category': 'Services/Project',
    'depends': ['project', 'sale_project'],
    'data': [
        'report/carta_reports.xml',
        'report/carta_fabricacion_template.xml',
        'report/carta_termino_fabricacion_template.xml',
        'report/carta_llegada_almacen_template.xml',
        'views/project_task_type_views.xml',
        'views/project_task_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'license': 'LGPL-3',
}
