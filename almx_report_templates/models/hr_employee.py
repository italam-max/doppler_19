from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    stock_location_id = fields.Many2one(
        'stock.location', string='Ubicación de Stock de IT',
        domain="[('usage', '=', 'internal')]",
        help='Ubicación interna donde está el equipo de IT asignado a este empleado.')
