{
    'name': 'Alamex - Acciones automatizadas',
    'version': '19.0.1.0.2',
    'summary': 'Acciones automatizadas de 16 versionadas como código (el upgrade a 19 las desactivó o las perdió)',
    'description': """
34 acciones automatizadas de Alamex en uso en 16 (actividad en los últimos 60 días),
revisadas y ajustadas para Odoo 19:

- Almacén/Compras: devoluciones, recepción de contenedores, seguimiento y analista de compras.
- Ventas/CRM: peticiones de mantenimiento desde la SO, recordatorios de Finanzas, Supply
  por contrato, tarea de Instalación/Modernización, cambios iniciativa/oportunidad.
- Mantenimiento: seguidor cliente, técnico/tipo preventivo, encuesta de satisfacción.
- Proyecto/Calidad/Helpdesk: plantillas de inspecciones y guías, actividades de Calidad
  Inst-Mod, seguidores, bloqueo de cierre de tickets.

Recrea además los campos de Studio que la automatización de mantenimiento necesita y que
el upgrade no conservó (línea y pedido de venta en la petición de mantenimiento).
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Productivity',
    'depends': [
        'base_automation', 'mail', 'survey', 'sale_management', 'sale_subscription', 'sale_project',
        'purchase', 'stock', 'crm', 'maintenance', 'project', 'quality_control', 'helpdesk',
        'approvals', 'almx_sale',
    ],
    'data': [
        'data/mail_data.xml',
        'views/maintenance_request_views.xml',
        'data/automation_almacen_compras.xml',
        'data/automation_ventas_crm.xml',
        'data/automation_mantenimiento.xml',
        'data/automation_proyecto_calidad_helpdesk.xml',
        'data/automation_triggers.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
