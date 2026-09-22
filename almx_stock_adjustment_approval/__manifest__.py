# -*- coding: utf-8 -*-
{
    'name': 'Alamex: Aprobación de Ajustes de Inventario',
    'version': '19.0.2.0.0',
    'summary': 'Flujo de aprobación para ajustes de inventario con historial y motivo',
    'category': 'Inventory',
    'author': 'Klivio IT / Irving Sammer',
    'depends': ['stock', 'mail'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/stock_adjustment_request_views.xml',
        'views/stock_adjustment_menu.xml',
        'wizard/stock_adjustment_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
