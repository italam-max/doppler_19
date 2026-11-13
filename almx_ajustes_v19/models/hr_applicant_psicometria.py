from odoo import fields, models


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    almx_machover = fields.Binary(string="Machover", attachment=True, copy=False)
    almx_machover_filename = fields.Char(string="Nombre de archivo Machover", copy=False)
    almx_man_in_rain = fields.Binary(string="Hombre bajo la lluvia", attachment=True, copy=False)
    almx_man_in_rain_filename = fields.Char(string="Nombre de archivo Hombre bajo la lluvia", copy=False)
    almx_zavic = fields.Binary(string="Zavic", attachment=True, copy=False)
    almx_zavic_filename = fields.Char(string="Nombre de archivo Zavic", copy=False)
    almx_psychometric_test = fields.Binary(string="Prueba psicométrica", attachment=True, copy=False)
    almx_psychometric_test_filename = fields.Char(string="Nombre de archivo Prueba psicométrica", copy=False)
    almx_iq = fields.Integer(string="IQ", copy=False)
