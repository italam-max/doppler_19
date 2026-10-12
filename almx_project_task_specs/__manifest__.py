{
    'name': "almx_project_task_specs",

    'summary': "ALAMEX: Caracteristicas del Proyecto (Ventas-Operaciones)",

    'description': """
Agrega una pestaña en el modulo de proyecto para las mesas de Guias mecanicas preliminares/definitivas, en la cuál especifica
los detalles de cada proyecto para los elevadores.
    """,

    'author': "Celia Hernandez",
    'website': "www.alam.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/project_task_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

