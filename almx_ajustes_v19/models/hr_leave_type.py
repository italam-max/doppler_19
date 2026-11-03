from odoo import api, fields, models
from odoo.fields import Domain


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    almx_restricted = fields.Boolean(
        string='Solo RH',
        default=True,
        help='Si está marcado, solo los usuarios del grupo '
             '"Tiempo personal: todos los tipos" (RH, IT y Dirección) pueden '
             'solicitar este tipo. Los demás empleados no lo ven al solicitar.',
    )

    @api.model
    def _almx_user_can_use_all_types(self):
        return self.env.is_superuser() or self.env.user.has_group(
            'almx_ajustes_v19.group_leave_all_types'
        )

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        if (self.env.context.get('almx_restrict_leave_types')
                and not self._almx_user_can_use_all_types()):
            domain = Domain(domain or Domain.TRUE) & Domain('almx_restricted', '=', False)
        return super().name_search(name, domain, operator, limit)
