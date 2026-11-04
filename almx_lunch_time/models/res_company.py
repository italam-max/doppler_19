# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.http import request


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _action_open_kiosk_mode(self):
        """En la app móvil el kiosko abre dentro de la app; en web sigue igual."""
        user_agent = request.httprequest.user_agent.string if request else ''
        if 'OdooMobile' in (user_agent or ''):
            return {
                'type': 'ir.actions.client',
                'tag': 'almx_lunch_time.kiosk_app',
                'name': _('Kiosk Mode'),
                'target': 'current',
            }
        return super()._action_open_kiosk_mode()
