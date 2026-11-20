# -*- coding: utf-8 -*-
from odoo import models

DEFAULT_MATRIX_LIMIT = 200


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _almx_matrix_limit(self):
        value = self.env['ir.config_parameter'].sudo().get_param(
            'almx_purchase_configurator.matrix_limit', DEFAULT_MATRIX_LIMIT)
        try:
            return int(value)
        except (TypeError, ValueError):
            return DEFAULT_MATRIX_LIMIT

    def _almx_use_configurator(self):
        """True si la matriz de compra sería demasiado grande para esta plantilla."""
        self.ensure_one()
        if not self.has_configurable_attributes:
            return False
        return self._get_matrix_combination_count() > self._almx_matrix_limit()

    def almx_purchase_use_configurator(self):
        """Llamado desde la línea de compra (JS) para decidir matriz o configurador."""
        self.ensure_one()
        return self._almx_use_configurator()
