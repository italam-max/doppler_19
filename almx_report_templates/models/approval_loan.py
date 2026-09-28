from odoo import fields, models


class ApprovalLoan(models.Model):
    _name = 'approval.loan'
    _description = 'Equipo de cómputo en solicitud de aprobación'

    # Nombres técnicos conservados desde 16 para que el upgrade preserve los datos.
    request_id = fields.Many2one(
        'approval.request', string='Solicitud de préstamo',
        ondelete='cascade', index=True, required=True)
    category_id = fields.Char(string='Categoría del equipo')
    model_id = fields.Char(string='Modelo del equipo')
    serial_number = fields.Char(string='Número de serie del equipo')
