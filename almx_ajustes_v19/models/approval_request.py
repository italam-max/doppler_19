from odoo import api, fields, models
from odoo.exceptions import UserError


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    # Estado "Hecho" que en 16 agregaba el módulo doppler (Vauxoo).
    request_status = fields.Selection(
        selection_add=[('done', 'Hecho')],
        ondelete={'done': 'set default'},
    )
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

    def action_done(self):
        not_approved = self.filtered(lambda r: r.request_status != 'approved')
        if not_approved:
            raise UserError(self.env._(
                'Solo se pueden marcar como hechas las solicitudes aprobadas: %s',
                ', '.join(not_approved.mapped('name')),
            ))
        self.write({'request_status': 'done'})
        return True
