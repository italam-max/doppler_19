from odoo import _, models
from odoo.exceptions import UserError

from .account_move import GRUPO_TIMBRADO


class L10nMxEdiDocument(models.Model):
    _inherit = 'l10n_mx_edi.document'

    def action_retry(self):
        """El botón Reintentar de un timbrado de factura fallido también timbra."""
        if not (self.env.su or self.env.user.has_group(GRUPO_TIMBRADO)) \
                and self.filtered(lambda d: d.state == 'invoice_sent_failed'):
            raise UserError(_(
                "El reintento de timbrado de facturas lo realiza el equipo de Finanzas."
            ))
        return super().action_retry()
