from odoo import fields, models


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    almx_attach_it_equipment = fields.Boolean(
        string='Adjuntar equipo de IT asignado',
        help='Al crear una solicitud en esta categoría se agregan automáticamente '
             'las laptops y cargadores que están en la ubicación de IT del solicitante.')
