# -*- coding: utf-8 -*-
from odoo import api, models


class ResGroups(models.Model):
    _inherit = 'res.groups'

    @api.model
    def action_almx_assign_manual_out_creators(self):
        """Reasigna los usuarios del grupo 'Alamex: Crear OUT manual
        (traslados)' buscándolos por login (correo).

        Se invoca desde security/security_groups.xml con una etiqueta
        <function>, por lo que corre tanto al instalar como en cada
        actualización del módulo -- así la asignación se restaura sola
        si el módulo llega a reinstalarse.
        """
        group = self.env.ref(
            'almx_stock_extends.group_almx_manual_out_creator',
            raise_if_not_found=False,
        )
        if not group:
            return

        logins = [
            'diego.u@alam.mx',
            'yazan@alam.mx',
            'hamdi@alam.mx',
            'celia.a@alam.mx',
            'alexis.a@alam.mx',
            'italam@alam.mx',
            'cesar.m@alam.mx',
        ]
        users = self.env['res.users'].search([('login', 'in', logins)])
        group.write({'users': [(6, 0, users.ids)]})
