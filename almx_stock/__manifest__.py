# -*- coding: utf-8 -*-
{
    'name': "Stock Modifications",

    'summary': """
        Modificaciones al módulo de stock y sus derivados
        -stock.picking
        -stock.moves
        -stock.move.lines""",

    'description': """
        Este módulo realiza modificaciones al módulo de stock y sus derivados, vistas y desarrollos

        Changelog:
        - 13.1: Corrige el campo "Dirección de entrega" (partner_only_dir) en el formulario de
          stock.picking, que compartía fila y etiqueta con partner_id asumiendo que nunca
          coexistirían para un mismo usuario. Se le da su propia fila y etiqueta explícita,
          y se elimina un campo partner_id duplicado que ya no era necesario.
        - 13.2: Quita la restricción de grupo (view_datos_partner_complete) sobre partner_id.
          No cumplía ningún otro propósito en el módulo y entraba en conflicto con un context
          nativo de Odoo que referencia partner_id en la vista de líneas de movimiento, lo cual
          impedía instalar/actualizar el módulo por línea de comandos (-u).
        - 13.3: Agrega el campo calculado address_display ("Dirección completa") en el formulario
          de stock.picking: arma calle/ciudad/estado/CP/país a partir de partner_only_dir o
          partner_id (el que tenga valor), sin exponer nombre/teléfono/otros datos del contacto.
          Campo no almacenado (se calcula al vuelo), visible para todos los usuarios.
    """,

    'author': "Alamex",
    'website': "https://alamex-mx.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '19.0.13.4',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'stock',
                'sale_stock',
                'almx_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/stock_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
