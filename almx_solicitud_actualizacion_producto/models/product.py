from datetime import timedelta

from markupsafe import Markup

from odoo import _, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_solicitar_actualizacion_producto(self):
        """Crea una actividad por tarea configurada a su responsable. No duplica
        si el producto ya tiene actividades de este proceso abiertas."""
        activity_type = self.env.ref(
            'almx_solicitud_actualizacion_producto.mail_activity_type_actualizacion_producto',
            raise_if_not_found=False)
        if not activity_type:
            raise UserError(_("No existe el tipo de actividad 'Actualización de Producto'."))
        tasks = self.env['almx.product.update.task'].sudo().search([])
        valid = tasks.filtered(lambda t: t.user_id and t.user_id.active)
        skipped = tasks - valid
        if not valid:
            raise UserError(_("No hay tareas de actualización con responsable activo. "
                              "Configúralas en Compras > Configuración."))

        Activity = self.env['mail.activity']
        model_id = self.env['ir.model']._get_id('product.template')
        today = fields.Date.context_today(self)
        con_proceso, nuevos, total = [], self.browse(), 0
        for product in self:
            if Activity.search_count([('res_model', '=', 'product.template'),
                                      ('res_id', '=', product.id),
                                      ('activity_type_id', '=', activity_type.id)], limit=1):
                con_proceso.append(product.display_name)
                continue
            nuevos |= product
            for task in valid:
                Activity.create({
                    'res_model_id': model_id,
                    'res_id': product.id,
                    'activity_type_id': activity_type.id,
                    'summary': task.name,
                    'note': Markup('<p>%s</p>') % (task.note or ''),
                    'date_deadline': today + timedelta(days=task.deadline_days),
                    'user_id': task.user_id.id,
                })
                total += 1

        if not nuevos:
            return self._almx_notify(_('⚠️ Proceso ya en curso'), _(
                "Estos productos ya tienen actividades de actualización pendientes: %s. "
                "Complétalas o cancélalas antes de iniciar un nuevo proceso.",
                ', '.join(con_proceso)), 'warning', sticky=True)

        msg = _("Se crearon %(n)s actividades para: %(p)s.", n=total, p=', '.join(nuevos.mapped('display_name')))
        kind, title = 'success', _('✅ Actualización solicitada')
        if con_proceso:
            msg += '\n' + _("Omitidos (ya tenían proceso en curso): %s.", ', '.join(con_proceso))
            kind, title = 'warning', _('⚠️ Proceso parcial')
        if skipped:
            msg += '\n' + _("Sin responsable activo (no se asignaron): %s.", ', '.join(skipped.mapped('name')))
            kind = 'warning'
        return self._almx_notify(title, msg, kind)

    def _almx_notify(self, title, message, kind, sticky=False):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': title, 'message': message, 'type': kind, 'sticky': sticky},
        }


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_solicitar_actualizacion_producto(self):
        return self.product_tmpl_id.action_solicitar_actualizacion_producto()
