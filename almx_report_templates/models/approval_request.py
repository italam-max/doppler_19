from odoo import Command, api, fields, models


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    approval_loan = fields.One2many(
        'approval.loan', 'request_id',
        string='Préstamo de equipo de cómputo', readonly=True)
    almx_attach_it_equipment = fields.Boolean(
        related='category_id.almx_attach_it_equipment')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.category_id.almx_attach_it_equipment and not rec.approval_loan:
                rec._almx_fill_it_equipment()
        return records

    def _almx_get_it_employee(self):
        """Empleado del solicitante (request_owner_id), priorizando la compañía de la solicitud."""
        self.ensure_one()
        user = self.request_owner_id or self.env.user
        employees = self.env['hr.employee'].sudo().search([('user_id', '=', user.id)])
        return employees.filtered(lambda e: e.company_id == self.company_id)[:1] or employees[:1]

    def _almx_fill_it_equipment(self):
        self.ensure_one()
        location = self._almx_get_it_employee().stock_location_id
        if not location:
            return
        # sudo: el solicitante normalmente no tiene permisos de Inventario.
        quants = self.env['stock.quant'].sudo().search([
            ('location_id', 'child_of', location.id),
            ('quantity', '>', 0),
            '|', ('product_id.is_laptop', '=', True), ('product_id.is_cargador', '=', True),
        ])
        lines = [
            Command.create({
                'category_id': 'Laptop' if q.product_id.is_laptop else 'Cargador',
                'model_id': q.product_id.display_name,
                'serial_number': q.lot_id.name or '',
            })
            for q in quants
        ]
        if lines:
            self.sudo().write({'approval_loan': lines})
