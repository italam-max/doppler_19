from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Nombre técnico conservado desde 16 para que el upgrade preserve el dato.
    x_studio_candidato = fields.Many2one('hr.applicant', string='Candidato', groups='hr.group_hr_user')
    almx_file_ids = fields.One2many('almx.employee.file', 'employee_id', string='Expediente', groups='hr.group_hr_user')
    almx_file_count = fields.Integer(compute='_compute_almx_file_count', groups='hr.group_hr_user')

    def _compute_almx_file_count(self):
        counts = dict(self.env['almx.employee.file']._read_group(
            [('employee_id', 'in', self.ids)], ['employee_id'], ['__count']))
        for employee in self:
            employee.almx_file_count = counts.get(employee, 0)

    def action_almx_open_files(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expediente',
            'res_model': 'almx.employee.file',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }
