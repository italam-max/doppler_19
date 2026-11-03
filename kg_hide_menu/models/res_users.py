# -*- coding: utf-8 -*-

# Klystron Global LLC
# Copyright (C) Klystron Global LLC
# All Rights Reserved
# https://www.klystronglobal.com/


from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Se conserva el mismo nombre de tabla relacional que la versión 16
    # para poder migrar los datos existentes sin cambios.
    hide_menu_access_ids = fields.Many2many(
        'ir.ui.menu', 'ir_ui_hide_menu_rel', 'uid', 'menu_id',
        string='Hide Access Menu')

    def write(self, vals):
        res = super().write(vals)
        if 'hide_menu_access_ids' in vals:
            # load_menus / load_menus_root / _visible_menu_ids están en caché (ormcache)
            self.env.registry.clear_cache()
        return res
