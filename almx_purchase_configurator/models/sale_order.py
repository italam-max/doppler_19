# -*- coding: utf-8 -*-
from odoo import _, models
from odoo.exceptions import AccessError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_almx_create_purchase(self):
        """Abre el asistente para crear la solicitud de compra con el equipo de esta venta."""
        self.ensure_one()
        if not self.env.user.has_group('almx_purchase_configurator.group_purchase_from_sale'):
            raise AccessError(_('Solo Compras puede crear solicitudes de compra desde la venta.'))
        if self.sale_type != 'project':
            raise UserError(_('Solo se crean solicitudes de compra desde ventas de Equipo Nuevo.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Crear solicitud de compra'),
            'res_model': 'almx.purchase.sale.copy',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_ref': self.name},
        }
