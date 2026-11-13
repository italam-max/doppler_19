from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    almx_require_comprobante = fields.Boolean(
        string='Requiere comprobante de entrega',
        help='Para validar se debe subir el Comprobante (hoja de entrega firmada, PDF o foto).',
    )
