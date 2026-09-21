from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order' #Herencia del módelo de ventas

    is_related = fields.Boolean(string='Obtener el tipo de movimiento', compute='relational_moves', default=False)

    def relational_moves(self):
        # ALMX FIX (blindaje enlace PICK/OUT manual): este compute no tiene
        # @api.depends, así que Odoo lo ejecuta cada vez que el campo
        # 'is_related' se lee -- en la práctica, cada vez que alguien abre
        # el formulario del pedido de venta, porque el campo está visible
        # ahí (sale_view.xml). La versión anterior buscaba pickings por
        # 'group_id', pero los PICK/OUT creados manualmente por las áreas
        # (ventas, laboratorio, operaciones) casi nunca tienen
        # procurement_group_id -- así que el filtro [('group_id','=', False)]
        # podía devolver pickings de CUALQUIER otra orden de venta sin
        # relación alguna, y 'auto_picks[0]'/'auto_outs[0]' tomaba el
        # primero de esa lista global, sobrescribiendo related_pick_id/
        # related_out_id con el PICK/OUT equivocado -- de otro pedido --
        # cada vez que se abría el formulario. Esto es lo que causó, por
        # ejemplo, que NWH/PICK/32418 (SO62568) mostrara related_out_id
        # apuntando a NWH/OUT/30644 (una OUT completamente distinta,
        # todavía en 'waiting').
        #
        # related_pick_id/related_out_id ahora se establecen ÚNICAMENTE
        # de forma explícita: por el botón "Crear OUT"/"Crear INT", o a
        # mano por el usuario en el propio traslado. Este compute se deja
        # solo como indicador informativo (is_related), sin efectos
        # secundarios sobre otros registros.
        for order in self:
            if not order.procurement_group_id:
                order.is_related = False
                continue
            pickings = self.env['stock.picking'].search([('group_id', '=', order.procurement_group_id.id)])
            auto_picks = pickings.filtered(lambda p: p.picking_type_id.sequence_code == 'NWH/PICK/')
            auto_outs = pickings.filtered(lambda p: p.picking_type_id.sequence_code == 'NWH/OUT/')
            order.is_related = bool(auto_picks and auto_outs)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    related_out_id = fields.Many2one('stock.picking', string='OUT relacionada', help='Muestra el movimiento relacionado', domain=[["picking_type_id.sequence_code","=","NWH/OUT/"]])
    related_pick_id = fields.Many2one('stock.picking', string='PICK relacionado', help='Muestra el movimiento relacionado', domain=[["picking_type_id.sequence_code","=","NWH/PICK/"]])
    #picking_id = fields.Many2many('stock.picking',string='OUT Complemento', help='Muestra los OUT complemento', domain=[["picking_type_id.sequence_code","=","OUT"]], index=True)
