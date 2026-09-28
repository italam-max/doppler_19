from markupsafe import Markup

from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Nombres técnicos conservados desde 16: los adjuntos se vuelven a ligar solos.
    format_finally = fields.Binary(string='Formatos Acabados', attachment=True)
    format_finally_filename = fields.Char()

    def _log_format_finally(self, action, filename):
        body = Markup(_('<b>Formatos Acabados</b>: archivo %(action)s "%(name)s".')) % {
            'action': action, 'name': filename or _('archivo')}
        for task in self:
            task.message_post(body=body)

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task in tasks.filtered('format_finally'):
            task._log_format_finally(_('subido'), task.format_finally_filename)
        return tasks

    def write(self, vals):
        logs = []
        if 'format_finally' in vals:
            new = vals.get('format_finally')
            for task in self:
                old, old_name = task.format_finally, task.format_finally_filename
                new_name = vals.get('format_finally_filename') or old_name
                if new:
                    logs.append((task, _('modificado') if old else _('subido'), new_name))
                elif old:
                    logs.append((task, _('eliminado'), old_name))
        res = super().write(vals)
        for task, action, name in logs:
            task._log_format_finally(action, name)
        return res
