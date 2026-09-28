from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    # Nombres técnicos conservados desde 16 para que el upgrade preserve los datos.
    in_process_request = fields.Boolean(string='Solicitud dentro del proceso', tracking=True)
    out_process_request = fields.Boolean(string='Solicitud fuera del proceso', tracking=True)
    process_reason = fields.Text(string='Motivo si salió de proceso', tracking=True)

    @api.onchange('in_process_request')
    def _onchange_in_process_request(self):
        if self.in_process_request:
            self.out_process_request = False
            self.process_reason = False

    @api.onchange('out_process_request')
    def _onchange_out_process_request(self):
        if self.out_process_request:
            self.in_process_request = False

    @api.constrains('in_process_request', 'out_process_request', 'process_reason')
    def _check_process_flags(self):
        for rec in self:
            if rec.in_process_request and rec.out_process_request:
                raise ValidationError(_('Una solicitud no puede estar dentro y fuera del proceso a la vez.'))
            if rec.out_process_request and not (rec.process_reason or '').strip():
                raise ValidationError(_('Indica el motivo por el que la solicitud salió de proceso.'))
