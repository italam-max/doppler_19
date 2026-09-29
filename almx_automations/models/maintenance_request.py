from odoo import fields, models


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    # Campos de Studio de 16 que el upgrade no conservó. Mismos nombres técnicos para la
    # automatización "Create Maintenance Request" y para el script de recuperación.
    x_studio_field_UT6zf = fields.Many2one('sale.order.line', string='Línea de pedido de venta', index=True)
    x_studio_field_ypPfL = fields.Many2one(related='x_studio_field_UT6zf.order_id', string='Pedido de venta', store=True)
