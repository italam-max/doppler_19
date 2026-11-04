from odoo import models


class SignRequest(models.Model):
    _inherit = 'sign.request'

    def almx_current_user_needs_to_sign(self):
        """Indica si el usuario actual tiene una firma pendiente en esta solicitud.

        Usa el mismo criterio que go_to_signable_document. Corre con sudo porque
        quien abre un enlace puede no tener acceso a las líneas de otros firmantes;
        solo devuelve un booleano sobre el propio usuario.
        """
        self.ensure_one()
        request = self.sudo().exists()
        partner = self.env.user.partner_id
        return bool(request.request_item_ids.filtered(
            lambda item: not item.partner_id or (item.state == 'sent' and item.partner_id == partner)
        ))
