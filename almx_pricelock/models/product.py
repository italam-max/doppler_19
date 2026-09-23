# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError

GROUP = 'almx_pricelock.group_edit_sale_price'
def _check_price_permission(env):
    if not env.su and not env.user.has_group(GROUP):
        # El texto se traduce aquí (en tiempo de ejecución, con env), no a nivel
        # de módulo: en 19 _() fuera de un env deja un warning en el log.
        raise UserError(env._("No tienes permiso para modificar el Precio de venta. "
                              "Solo el grupo 'Editar precio de venta' puede hacerlo."))


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # list_price ya tiene tracking=True de forma nativa en 19.

    def write(self, vals):
        if 'list_price' in vals:
            _check_price_permission(self.env)
        return super().write(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    variant_price = fields.Float(
        string='Precio de venta (variante)',
        digits='Product Price',
        tracking=True,
        help='Precio de venta propio de esta variante, independiente del precio base '
             'del producto y de las demás variantes. En 0 se usa el cálculo nativo '
             '(precio base + extras de atributos).',
    )

    def write(self, vals):
        if 'variant_price' in vals or 'lst_price' in vals:
            _check_price_permission(self.env)
        return super().write(vals)

    @api.depends('list_price', 'price_extra', 'variant_price')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        super()._compute_product_lst_price()
        to_uom = self.env['uom.uom'].browse(self.env.context['uom']) if 'uom' in self.env.context else None
        for product in self.filtered('variant_price'):
            price = product.variant_price
            if to_uom:
                price = product.uom_id._compute_price(price, to_uom)
            product.lst_price = price

    def _set_product_lst_price(self):
        """En vez de propagar al precio base de la plantilla (nativo), guarda el
        precio en la propia variante. Así editar una variante nunca mueve la
        plantilla ni las demás variantes."""
        for product in self:
            if self.env.context.get('uom'):
                value = self.env['uom.uom'].browse(self.env.context['uom'])._compute_price(
                    product.lst_price, product.uom_id)
            else:
                value = product.lst_price
            product.write({'variant_price': value})

    def _price_compute(self, price_type, uom=None, currency=None, company=None, date=False):
        """Listas de precios / pedidos de venta: si la variante tiene precio propio,
        se usa ese en lugar de precio base + extras."""
        prices = super()._price_compute(price_type, uom=uom, currency=currency, company=company, date=date)
        if price_type != 'list_price':
            return prices
        company = company or self.env.company
        date = date or fields.Date.context_today(self)
        for product in self.with_company(company).filtered('variant_price'):
            price = product.variant_price
            if uom:
                price = product.uom_id._compute_price(price, uom)
            if currency:
                price = product.currency_id._convert(price, currency, company, date)
            prices[product.id] = price
        return prices
