# -*- coding: utf-8 -*-
import base64
from odoo import _, api, fields, models
from odoo import api, SUPERUSER_ID
from odoo.exceptions import UserError
from datetime import datetime
from pytz import timezone
import logging
import json
import requests


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    collect_date = fields.Datetime(string='Fecha de recolección',
                                   help='Fecha de recolección para una recolección programada', tracking=True)
    carrier_id = fields.Many2one('delivery.carrier', string='Método de entrega',
                                 help='Método de entrega para la orden de venta', tracking=True)
    is_immediate = fields.Boolean(string='Es entrega inmediata?',
                                  help='Muestra si la órden de venta está configurada para entrega inmediata')
    sale_type = fields.Selection([('project', 'Equipo Nuevo'),
                                  ('spare', 'Refacciones'),
                                  ('mantto', 'Mantenimiento'),
                                  ('modern', 'Modernización'),
                                  ('fix', 'Reparación'),],
                                 string='Tipo de venta', help='Muestra el tipo de venta que designa el vendedor', tracking=True)
    completely_paid = fields.Boolean(string='Venta Pagada', help='Muestra si el equipo de finanzas confirmó el pago de la SO', tracking=True, groups='almx_sale.group_can_confirm_sale_payment')
    # ALMX (sept 2026): usuarios de TI/Direccion (almx_sale.group_so_admin) son
    # los unicos que pueden cancelar o eliminar pedidos de venta, y los unicos
    # que pueden cambiar el Tipo de venta una vez confirmado el pedido.
    is_so_admin = fields.Boolean(string='Es administrador de ventas', compute='_compute_is_so_admin')

    @api.depends_context('uid')
    def _compute_is_so_admin(self):
        is_admin = self.env.user.has_group('almx_sale.group_so_admin')
        for rec in self:
            rec.is_so_admin = is_admin

    def _almx_is_so_admin(self):
        return self.env.su or self.env.user.has_group('almx_sale.group_so_admin')

    def write(self, vals):
        if 'sale_type' in vals and not self._almx_is_so_admin():
            locked = self.filtered(lambda o: o.state == 'sale' and o.sale_type != vals['sale_type'])
            if locked:
                raise UserError(_("El Tipo de venta no se puede modificar una vez confirmado el pedido (%s). "
                                  "Solicítalo al área de TI.") % ', '.join(locked.mapped('name')))
        return super().write(vals)

    def action_cancel(self):
        if not self._almx_is_so_admin():
            raise UserError(_("Solo el área de TI puede cancelar pedidos de venta."))
        return super().action_cancel()

    def _action_cancel(self):
        if not self._almx_is_so_admin():
            raise UserError(_("Solo el área de TI puede cancelar pedidos de venta."))
        return super()._action_cancel()

    def unlink(self):
        if not self._almx_is_so_admin():
            raise UserError(_("Solo el área de TI puede eliminar pedidos de venta."))
        return super().unlink()

    @api.onchange('carrier_id')
    def is_immediate_carrier(self):
        carrier = self.env['delivery.carrier'].search([('id', '=', self.carrier_id.id)], limit=1)
        carrier_name = carrier.name
        carrier_id = carrier.id
        if carrier_name == 'Recolección Programada':
            self.is_immediate = True
        else:
            self.is_immediate = False

    # @api.model
    # def create(self, values):
    #    sale_order = super(SaleOrder, self).create(values)
    #    sale_order.is_immediate_carrier()  # Llamar al método al crear la SO
    #    return sale_order
    #
    # def write(self, values):
    #    res = super(SaleOrder, self).write(values)
    #    if 'carrier_id' in values:
    #        self.is_immediate_carrier()  # Llamar al método al modificar la SO
    #    return res