from odoo import fields, models

SHIPPING_KINDS = [
    ('paqueteria', 'Paquetería'),
    ('flete', 'Flete'),
    ('inmediata', 'Entrega inmediata'),
    ('recoleccion', 'Recolección programada'),
    ('app', 'Servicio de app'),
    ('proyecto', 'Proyecto Alamex'),
]


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    almx_shipping_kind = fields.Selection(
        SHIPPING_KINDS, string='Tipo de método Alamex',
        help='Decide qué datos se piden en la venta para este método de envío.')
