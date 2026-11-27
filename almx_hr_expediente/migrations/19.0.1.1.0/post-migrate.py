from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    from odoo.addons.almx_hr_expediente.models.hr_employee import seed_psico_from_applicants
    seed_psico_from_applicants(api.Environment(cr, SUPERUSER_ID, {}))
