# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    require_serial_confirmation = fields.Boolean(
        string='Requiere confirmación manual de número de serie',
        default=False,
        help=(
            "Si está activo, al validar un traslado de este tipo que tenga "
            "productos con seguimiento por número de serie, se pedirá "
            "capturar manualmente el número de serie a entregar y se "
            "verificará contra los números de serie dados de alta antes "
            "de permitir la validación. Pensado para el paso de Recogida "
            "(PICK), donde el operador toma físicamente el producto."
        ),
    )
