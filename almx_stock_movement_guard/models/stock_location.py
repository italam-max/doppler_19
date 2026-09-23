from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    almx_requires_direction = fields.Boolean(
        string='Requiere autorización de Dirección',
        help='Cualquier traslado con destino a esta ubicación (o a una de sus '
             'sububicaciones) solo lo puede validar el grupo Dirección.',
    )
    almx_asset_location = fields.Boolean(
        string='Ubicación de asignación de equipo',
        help='Destino válido para los tipos de operación de Asignación de equipo '
             '(incluye sus sububicaciones, p. ej. una por empleado).',
    )
