from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # En 16 lo daba almx_project (deprecado en 19); se recupera con _data_recovery.
    end_guides = fields.Char('Guías terminadas (referencia)')
