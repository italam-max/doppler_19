from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    # Nombres técnicos conservados desde 16 para que el upgrade preserve los datos.
    start_date = fields.Datetime(string='Fecha de inicio programada', tracking=True)
    effective_date = fields.Datetime(string='Fecha efectiva de término', tracking=True)
    end_date = fields.Datetime(string='Fecha de fin', tracking=True)
    almx_show_structural_dates = fields.Boolean(related='team_id.almx_structural_dates')


class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    almx_structural_dates = fields.Boolean(
        string='Fechas de elevación estructural',
        help='Muestra en los tickets de este equipo las fechas de inicio programada, término efectivo y fin.')
