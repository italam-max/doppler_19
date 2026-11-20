# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.exceptions import UserError

# Conversaciones (chats/canales) quedan fuera del candado.
ALMX_UNLOCKED_MODELS = ('discuss.channel',)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _almx_can_edit_chatter(self):
        self.ensure_one()
        return self.has_group('almx_chatter_lock.group_chatter_edit')

    def _almx_check_chatter_lock(self, model_names):
        """Lanza error si el usuario no está exento y algún modelo está bajo candado."""
        self.ensure_one()
        if not any(m and m not in ALMX_UNLOCKED_MODELS for m in model_names):
            return
        if self._almx_can_edit_chatter():
            return
        raise UserError(_(
            "Por política de Dirección no se pueden editar ni eliminar mensajes "
            "del chatter ni sus adjuntos. Si necesitas una corrección, agrega una "
            "nota nueva o solicítalo a Sistemas."
        ))
