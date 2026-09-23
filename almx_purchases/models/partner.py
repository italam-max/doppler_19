from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    almx_import_vendor = fields.Boolean(
        string='Proveedor de importación',
        help='Sus compras llegan con pedimento: en las recepciones se exige el número '
             'de pedimento.',
    )
