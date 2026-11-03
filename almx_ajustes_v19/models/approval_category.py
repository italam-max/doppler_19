from odoo import fields, models


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    # Mismos nombres y tabla de relación que el módulo doppler de 16,
    # para recuperar los datos por id sin transformaciones.
    read_group_ids = fields.Many2many(
        'res.groups',
        'approval_category_read_groups',
        'approval_category_id',
        'res_group_id',
        string='Grupos de lectura',
        help='Solo los usuarios de estos grupos ven la categoría. '
             'Si se deja vacío, la ven todos los usuarios internos.',
    )
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsable',
        help='Responsable que se asigna por defecto a las solicitudes de esta categoría.',
    )
