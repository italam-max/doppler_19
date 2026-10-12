# from odoo import models, fields, api


# class almx_project_task_specs(models.Model):
#     _name = 'almx_project_task_specs.almx_project_task_specs'
#     _description = 'almx_project_task_specs.almx_project_task_specs'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

