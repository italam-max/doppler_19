from odoo import SUPERUSER_ID, api

from odoo.addons.almx_pick_out_flow import almx_set_comprobante_types


def migrate(cr, version):
    almx_set_comprobante_types(api.Environment(cr, SUPERUSER_ID, {}))
