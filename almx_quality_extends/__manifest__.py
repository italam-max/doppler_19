{
    'name': 'Alamex - Calidad: Número de Pedimento',
    'version': '19.0.1.0.0',
    'summary': 'Liga el número de pedimento de la recepción a las alertas de calidad',
    'description': """
Alamex - Calidad: Número de Pedimento
======================================

Agrega el campo "Número de Pedimento" (entry_number) a las Alertas de Calidad
(quality.alert), heredado directamente de la recepción (stock.picking) que
originó la alerta.

Objetivo (solicitado por el equipo de Calidad):
  * Poder identificar, desde la propia alerta de calidad, en qué contenedor
    ingresó la mercancía (dato que determina el número de pedimento).
  * Poder filtrar y agrupar alertas de calidad por número de pedimento.

Implementación:
  * Campo relacionado y almacenado (related + store=True) sobre
    picking_id.entry_number. No requiere captura manual: si la alerta tiene
    una recepción ligada (picking_id), el número de pedimento se completa
    solo y queda indexado para filtros/agrupaciones.
  * Visible en el formulario (junto a la Transferencia), en la lista
    (columna opcional) y disponible como filtro/agrupador en la búsqueda.

Depende de almx_purchases porque ahí vive el campo base entry_number en
stock.picking.
    """,
    'author': 'Alamex Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Manufacturing/Quality',
    'depends': [
        'quality_control',
        'almx_purchases',
    ],
    'data': [
        'views/quality_alert_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
