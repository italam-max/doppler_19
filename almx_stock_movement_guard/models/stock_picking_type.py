from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    almx_require_sale_order = fields.Boolean(
        string='Requiere Pedido de venta',
        help='No se puede validar un traslado de este tipo sin un Pedido de venta '
             'confirmado ligado. Pensado para PICK y OUT.',
    )
    almx_guard_receipts = fields.Boolean(
        string='Candado de recepciones',
        help='Solo se validan libremente las recepciones que vienen de una Orden de '
             'compra o que son devoluciones nativas (botón Devolver). Cualquier otra '
             'solo la valida Dirección.',
    )
    almx_asset_assignment = fields.Boolean(
        string='Asignación de equipo',
        help='Solo el grupo Asignación de equipo (TI / RH) puede validar este tipo, y '
             'solo hacia ubicaciones marcadas como Ubicación de asignación.',
    )
    almx_freeze_lines = fields.Boolean(
        string='Congelar contenido (solo lo del pedido)',
        help='Una vez confirmado el traslado no se pueden agregar ni borrar líneas, '
             'cambiar producto ni cantidad pedida, ni validar más de lo pedido. Si el '
             'pedido está mal, se cancela la SO y se hace otra. Pensado para OUT.',
    )
