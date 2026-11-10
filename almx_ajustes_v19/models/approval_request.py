from odoo import api, fields, models
from odoo.exceptions import UserError

# Grupo que puede cambiar el responsable de una solicitud (Sammer y Hamdi)
GROUP_CHANGE_RESPONSIBLE = 'almx_ajustes_v19.group_approval_change_responsible'


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    # Estado "Hecho" que en 16 agregaba el módulo doppler (Vauxoo).
    request_status = fields.Selection(
        selection_add=[('done', 'Hecho')],
        ondelete={'done': 'set default'},
    )
    # Responsable = quien ejecuta al final (aplica el pago, la dispersión, la nota
    # de crédito...), no quien aprueba. Se toma de la categoría.
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsable',
        compute='_compute_responsible_id',
        store=True,
        readonly=False,
        tracking=True,
    )

    @api.depends('category_id')
    def _compute_responsible_id(self):
        for request in self:
            # Si la categoría no tiene responsable se conserva el valor actual.
            request.responsible_id = (
                request.category_id.responsible_id or request.responsible_id
            )

    # ------------------------------------------------------------------
    # Responsable fijo: solo el grupo "Puede cambiar el responsable" lo edita
    # ------------------------------------------------------------------
    def _almx_can_change_responsible(self):
        return self.env.su or self.env.user.has_group(GROUP_CHANGE_RESPONSIBLE)

    @api.model_create_multi
    def create(self, vals_list):
        if not self._almx_can_change_responsible():
            categories = self.env['approval.category']
            for vals in vals_list:
                category = categories.browse(vals.get('category_id'))
                if category.responsible_id:
                    vals['responsible_id'] = category.responsible_id.id
        return super().create(vals_list)

    def write(self, vals):
        if 'responsible_id' in vals and not self._almx_can_change_responsible():
            new_category = self.env['approval.category'].browse(vals.get('category_id'))
            for request in self:
                category = new_category or request.category_id
                allowed = {request.responsible_id.id, category.responsible_id.id}
                if (vals['responsible_id'] or False) not in allowed:
                    raise UserError(self.env._(
                        'El responsable lo define la categoría "%s". '
                        'Solo IT o Dirección pueden cambiarlo.', category.name,
                    ))
        return super().write(vals)

    # ------------------------------------------------------------------
    # Aviso al responsable cuando la solicitud queda aprobada
    # ------------------------------------------------------------------
    def action_approve(self, *args, **kwargs):
        before = {request.id: request.request_status for request in self}
        res = super().action_approve(*args, **kwargs)
        approved = self.filtered(
            lambda r: r.request_status == 'approved' and before.get(r.id) != 'approved'
        )
        approved._almx_schedule_responsible_activity()
        return res

    def _almx_schedule_responsible_activity(self):
        for request in self.filtered('responsible_id'):
            # sudo: quien aprueba no siempre tiene permiso de escritura sobre la solicitud
            request.sudo().activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=request.responsible_id.id,
                summary=self.env._('Aplicar solicitud aprobada'),
                note=self.env._(
                    'La solicitud fue aprobada. Aplícala (pago, dispersión, nota de '
                    'crédito, etc.) y márcala como hecha.'
                ),
            )

    def action_done(self):
        not_approved = self.filtered(lambda r: r.request_status != 'approved')
        if not_approved:
            raise UserError(self.env._(
                'Solo se pueden marcar como hechas las solicitudes aprobadas: %s',
                ', '.join(not_approved.mapped('name')),
            ))
        self.write({'request_status': 'done'})
        # Cierra la actividad "Aplicar solicitud aprobada" del responsable
        for request in self.filtered('responsible_id'):
            request.sudo().activity_feedback(
                ['mail.mail_activity_data_todo'],
                user_id=request.responsible_id.id,
                feedback=self.env._('Marcada como hecha'),
            )
        return True
