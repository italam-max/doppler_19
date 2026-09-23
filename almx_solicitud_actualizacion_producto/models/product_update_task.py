from odoo import fields, models


class AlmxProductUpdateTask(models.Model):
    _name = 'almx.product.update.task'
    _description = 'Tarea de actualización de producto'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    name = fields.Char(string='Tarea', required=True)
    user_id = fields.Many2one('res.users', string='Responsable')
    deadline_days = fields.Integer(string='Plazo (días)', default=3)
    note = fields.Text(string='Instrucciones')
