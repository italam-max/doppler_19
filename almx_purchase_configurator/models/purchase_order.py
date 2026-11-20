# -*- coding: utf-8 -*-
from odoo import _, api, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('grid_product_tmpl_id')
    def _set_grid_up(self):
        # Candado: armar la matriz de estas plantillas agota la memoria del worker.
        template = self.grid_product_tmpl_id
        if template and template._almx_use_configurator():
            raise UserError(_(
                "%(product)s tiene demasiadas combinaciones para la matriz. "
                "Recarga la página y vuelve a seleccionarlo: se abrirá el "
                "configurador de producto.", product=template.display_name))
        return super()._set_grid_up()

    def action_almx_copy_from_sale(self):
        self.ensure_one()
        if not self.env.user.has_group('almx_purchase_configurator.group_purchase_from_sale'):
            raise UserError(_('Solo Compras puede copiar el equipo de la venta.'))
        if self.state not in ('draft', 'sent'):
            raise UserError(_('Solo se pueden agregar productos a solicitudes de cotización (borrador o enviadas).'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Copiar equipo de la venta'),
            'res_model': 'almx.purchase.sale.copy',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_purchase_id': self.id},
        }

    def get_report_matrixes(self):
        """Igual que purchase_product_matrix, pero sin las plantillas demasiado
        grandes (sus líneas se imprimen normal)."""
        big = self.order_line.product_template_id.filtered(
            lambda t: t._almx_use_configurator())
        if not big:
            return super().get_report_matrixes()
        matrixes = []
        if self.report_grids:
            templates = self.order_line.filtered('is_configurable_product').product_template_id - big
            for template in templates:
                if len(self.order_line.filtered(lambda l: l.product_template_id == template)) > 1:
                    matrix = self._get_matrix(template)
                    matrix['matrix'] = [
                        row for row in matrix['matrix']
                        if any(column['qty'] != 0 for column in row[1:])
                    ]
                    matrixes.append(matrix)
        return matrixes
