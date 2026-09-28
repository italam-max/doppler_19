from odoo import fields, models

CARTA_CODES = [
    ('fabricacion', 'MEX-OPE-ANX-07 Carta de Confirmación de Fabricación'),
    ('termino_fabricacion', 'MEX-OPE-ANX-08 Carta de Término de Fabricación'),
    ('llegada_almacen', 'MEX-OPE-ANX-09 Carta de Llegada de Equipo a Almacén'),
]


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    almx_carta_code = fields.Selection(
        CARTA_CODES, string='Carta a generar',
        help='Carta que se genera al llegar a esta etapa desde alguna de las etapas de origen.')
    almx_carta_origin_stage_ids = fields.Many2many(
        'project.task.type', 'almx_carta_stage_origin_rel', 'stage_id', 'origin_id',
        string='Etapas de origen de la carta')
