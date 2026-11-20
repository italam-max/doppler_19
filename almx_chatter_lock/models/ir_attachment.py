# -*- coding: utf-8 -*-
from odoo import models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def _delete_and_notify(self, message=None):
        # /mail/attachment/delete llama esto con sudo y con el mensaje cuando el
        # adjunto ya está publicado; sin mensaje = adjunto aún en el editor.
        if message:
            self.env.user._almx_check_chatter_lock([message.sudo().model])
        return super()._delete_and_notify(message=message)
