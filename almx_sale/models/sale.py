# -*- coding: utf-8 -*-
import base64
from odoo import _, api, fields, models
from odoo import api, SUPERUSER_ID
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