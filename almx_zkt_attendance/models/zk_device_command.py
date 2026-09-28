# -*- coding: utf-8 -*-
from odoo import fields, models


class ZkDeviceCommand(models.Model):
    _name = 'zk.device.command'
    _description = 'Comando ADMS enviado (o por enviar) a una terminal ZKTeco'
    _order = 'create_date desc'

    device_id = fields.Many2one(
        'zk.device', string='Terminal', required=True, ondelete='cascade')
    command = fields.Char(
        string='Comando', required=True,
        help='Línea de comando ADMS, ej. "SET OPTIONS DateTime=2026-07-31 12:30:00". '
             'No incluir el prefijo "C:<id>:", eso se arma automáticamente al enviarlo.')
    state = fields.Selection([
        ('pending', 'Pendiente de envío'),
        ('sent', 'Enviado, esperando confirmación'),
        ('done', 'Confirmado por el equipo'),
        ('error', 'El equipo reportó error'),
    ], string='Estado', default='pending', required=True)
    seq = fields.Integer(
        string='ID de comando (ADMS)', readonly=True,
        help='Número de secuencia con el que se identificó este comando frente '
             'al equipo (protocolo ADMS "C:<seq>:..."). Se usa para casar la '
             'confirmación que regrese la terminal.')
    sent_date = fields.Datetime(string='Enviado el', readonly=True)
    ack_date = fields.Datetime(string='Confirmado el', readonly=True)
    raw_ack = fields.Text(
        string='Respuesta cruda del equipo', readonly=True,
        help='Se guarda tal cual para poder confirmar/ajustar el formato exacto '
             'de confirmación que usa este firmware.')
