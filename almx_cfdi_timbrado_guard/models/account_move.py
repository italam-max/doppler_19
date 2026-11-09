from odoo import _, api, fields, models
from odoo.exceptions import UserError

GRUPO_TIMBRADO = 'almx_cfdi_timbrado_guard.group_timbrar_cfdi'


class AccountMove(models.Model):
    _inherit = 'account.move'

    almx_bloquear_envio = fields.Boolean(
        string='Envío bloqueado (sin Folio Fiscal)',
        compute='_compute_almx_bloquear_envio',
    )

    def _almx_pendientes_de_timbrar(self):
        """Facturas/notas de crédito de cliente MX, registradas y sin Folio Fiscal."""
        return self.filtered(
            lambda m: m.move_type in ('out_invoice', 'out_refund')
            and m.state == 'posted'
            and m.country_code == 'MX'
            and not m.l10n_mx_edi_cfdi_uuid
        )

    @api.model
    def _almx_puede_timbrar(self):
        return self.env.su or self.env.user.has_group(GRUPO_TIMBRADO)

    @api.depends_context('uid')
    @api.depends('state', 'move_type', 'company_id', 'l10n_mx_edi_cfdi_uuid')
    def _compute_almx_bloquear_envio(self):
        puede = self._almx_puede_timbrar()
        pendientes = self._almx_pendientes_de_timbrar()
        for move in self:
            move.almx_bloquear_envio = not puede and move in pendientes

    def _almx_check_timbrado(self):
        if self._almx_puede_timbrar():
            return
        pendientes = self._almx_pendientes_de_timbrar()
        if pendientes:
            raise UserError(_(
                "No puedes enviar estas facturas porque aún no tienen Folio Fiscal: %s\n\n"
                "El envío y timbrado ante el SAT lo realiza el equipo de Finanzas. "
                "Una vez timbradas, podrás reenviarlas al cliente.",
                ", ".join(pendientes.mapped('name')),
            ))

    # Formulario (botones "Enviar")
    def action_invoice_sent(self):
        self._almx_check_timbrado()
        return super().action_invoice_sent()

    # Lista / envío masivo (botón "Send" del encabezado y acciones que lo llamen)
    def action_send_and_print(self):
        self._almx_check_timbrado()
        return super().action_send_and_print()
