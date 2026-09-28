from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_it = fields.Boolean(string='Equipo de IT', help='Indica si el producto es equipo de cómputo/IT')
    is_laptop = fields.Boolean(string='¿Es laptop?')
    is_cargador = fields.Boolean(string='¿Es cargador?')
