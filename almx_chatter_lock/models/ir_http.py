# -*- coding: utf-8 -*-
from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super().session_info()
        user = self.env.user
        result['almx_can_edit_chatter'] = bool(user and user._almx_can_edit_chatter())
        return result
