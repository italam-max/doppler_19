import logging

from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
GROUP = 'almx_strict_product_lock.group_allow_product_creation'


def _check_can_create(env, what):
    if env.su or env.user.has_group(GROUP):
        return
    _logger.info("Alta de %s bloqueada para el usuario %s (%s)", what, env.user.name, env.user.id)
    raise UserError(env._(
        "⛔ ACCIÓN DENEGADA\n\n"
        "No tienes permisos para crear nuevos productos.\n"
        "La creación de catálogo está restringida exclusivamente a Dirección y T.I.\n\n"
        "Si crees que esto es un error, solicita al administrador que te asigne el "
        "permiso 'Permitir Crear Productos'."
    ))


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        _check_can_create(self.env, 'producto')
        return super().create(vals_list)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        _check_can_create(self.env, 'variante')
        return super().create(vals_list)
