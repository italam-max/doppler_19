# -*- coding: utf-8 -*-
from odoo import models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _check_can_update_message_content(self, messages):
        # Cubre editar y "eliminar" desde el chatter: en 19 ambos pasan por
        # /mail/message/update_content -> _message_update_content(strict=True).
        if not self.env.su:
            self.env.user._almx_check_chatter_lock([self._name])
        return super()._check_can_update_message_content(messages)
