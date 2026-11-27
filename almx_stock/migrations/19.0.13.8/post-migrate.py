from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Traslados manuales con SO en Documento origen: recalcula tipo de venta y pagado."""
    env = api.Environment(cr, SUPERUSER_ID, {'tracking_disable': True, 'active_test': False})
    Picking = env['stock.picking']
    recs = Picking.search([('sale_id', '=', False), ('almx_origin_sale_id', '!=', False)])
    for fname in ('x_studio_tipo_de_venta', 'x_studio_completamente_pagado'):
        env.add_to_compute(Picking._fields[fname], recs)
    env.flush_all()
