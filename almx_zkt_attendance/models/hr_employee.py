# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    zk_pin = fields.Char(
        string='PIN checador ZKTeco', copy=False,
        help='Número de enrolamiento (PIN) configurado en la terminal ZKTeco para este empleado. '
             'Debe coincidir exactamente con el PIN capturado en el equipo al dar de alta su huella/tarjeta.')

    # En 19 `_sql_constraints` ya no se aplica (solo loguea un warning): se usa models.Constraint.
    _zk_pin_uniq = models.Constraint(
        'unique(zk_pin)', 'Ya existe otro empleado con ese PIN de checador.')
