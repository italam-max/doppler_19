from odoo import api, fields, models


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    # Nombre técnico conservado desde 16 para que el upgrade preserve los datos.
    x_studio_po_1 = fields.Many2one('purchase.order', string='PO')

    # En 16 era x_studio_field_eEfAE (Many2one a hr.expense.sheet). El Informe de
    # gastos ya no existe en 19: se liga directamente a los gastos.
    almx_expense_ids = fields.Many2many(
        'hr.expense', 'almx_approval_request_hr_expense_rel', 'request_id', 'expense_id',
        string='Gastos', domain="[('company_id', '=', company_id)]")

    is_in_group = fields.Boolean(
        string='¿Es Contabilidad / Administrador?', compute='_compute_is_in_group',
        help='Permite editar "Pagado" solo a Contabilidad / Administrador.')

    @api.depends_context('uid')
    def _compute_is_in_group(self):
        is_manager = self.env.user.has_group('account.group_account_manager')
        for rec in self:
            rec.is_in_group = is_manager
