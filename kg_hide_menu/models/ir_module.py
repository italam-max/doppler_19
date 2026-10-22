# -*- coding: utf-8 -*-

# Klystron Global LLC
# Copyright (C) Klystron Global LLC
# All Rights Reserved
# https://www.klystronglobal.com/


from odoo import models


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def _visible_menu_ids(self, debug=False):
        # El super está en caché (ormcache por grupos del usuario): nunca se
        # debe modificar el set devuelto, se regresa una copia nueva.
        visible = super()._visible_menu_ids(debug)
        user = self.env.user
        if user.hide_menu_access_ids and not user.has_group('base.group_system'):
            visible = visible - set(user.hide_menu_access_ids.ids)
        return visible
