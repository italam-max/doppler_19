# -*- coding: utf-8 -*-
from odoo import fields, models


class QualityAlert(models.Model):
    _inherit = 'quality.alert'

    entry_number = fields.Char(
        string='Número de Pedimento',
        related='picking_id.entry_number',
        store=True,
        readonly=True,
        help=(
            "Número de pedimento capturado en la recepción (Transferencia) "
            "que originó esta alerta de calidad. Determina en qué "
            "contenedor ingresó la mercancía. Se completa automáticamente "
            "a partir de la transferencia ligada; no es editable aquí."
        ),
    )
