from odoo import fields, models

CATEGORIAS = [(v, v) for v in [
    'Cliente de Refacciones', 'Cliente de Sistemas de Elevación', 'Cliente de Instalaciones',
    'Cliente de Mantenimiento', 'Cliente de Reparaciones', 'Proveedor', 'Proveedor Nacional',
    'Empleado', 'Usuario', 'Usuario de Portal', 'Otros',
]]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # En 16 era un campo de Studio que el upgrade a 19 no conservó. Mismo nombre técnico y
    # mismos valores para que el script de recuperación sea directo.
    x_studio_categoria_comercial = fields.Selection(CATEGORIAS, string='Categoría comercial', tracking=True)
