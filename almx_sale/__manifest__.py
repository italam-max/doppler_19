# -*- coding: utf-8 -*-
{
    'name': "Sale Modifications",

    'summary': """
        Modificaciones al módulo de ventas""",

    'description': """
        Este módulo agrega modificaciones personalizadas al modelo sale.order
        
            -Vistas
            -Campos
            -Modelos
            -Modelos relacionados (sale.order.line)
    """,

    'author': "Alamex",
    'website': "https://www.alamx.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '19.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','delivery'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security_groups.xml',
        'views/sale_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
