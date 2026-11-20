# -*- coding: utf-8 -*-
from odoo import models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    def unlink(self):
        # Los procesos internos de Odoo borran mensajes con sudo; esos pasan.
        if not self.env.su and self:
            self.env.user._almx_check_chatter_lock(set(self.mapped('model')))
        return super().unlink()
