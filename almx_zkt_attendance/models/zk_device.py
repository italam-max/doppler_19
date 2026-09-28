# -*- coding: utf-8 -*-
from datetime import datetime

import pytz

from odoo import fields, models


class ZkDevice(models.Model):
    _name = 'zk.device'
    _description = 'Terminal ZKTeco (checador ADMS)'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True, help='Ej. "F22 - Almacén NWH"')
    serial_number = fields.Char(
        string='Número de serie (SN)', required=True, copy=False,
        help='Se consulta en el equipo en Menú > Sistema Info > Info del Dispositivo, '
             'o en Menú > Comm > Ethernet.')
    active = fields.Boolean(default=True)
    tz = fields.Selection(
        selection='_get_tz_selection', string='Zona horaria del equipo',
        default='America/Mexico_City', required=True,
        help='Zona horaria con la que la terminal reporta sus marcajes.')
    last_seen = fields.Datetime(string='Último contacto', readonly=True)
    last_attlog_stamp = fields.Char(string='Último stamp ATTLOG', readonly=True, default='None')
    location_note = fields.Char(string='Ubicación / notas')

    cmd_seq_counter = fields.Integer(
        string='Contador de comandos ADMS', default=0, readonly=True,
        help='Último número de secuencia usado para identificar comandos '
             'frente a este equipo (protocolo ADMS "C:<seq>:...").')
    command_ids = fields.One2many(
        'zk.device.command', 'device_id', string='Comandos ADMS')

    allowed_ips = fields.Char(
        string='IPs permitidas',
        help='Opcional. IPs públicas desde las que se aceptan checadas de este equipo, '
             'separadas por coma (ej. la IP pública del Meraki de la sucursal). '
             'Vacío = se acepta desde cualquier IP (comportamiento de 16).')

    _serial_number_uniq = models.Constraint(
        'unique(serial_number)', 'Ya existe una terminal registrada con ese número de serie.')

    def _almx_ip_allowed(self, remote_addr):
        self.ensure_one()
        ips = [ip.strip() for ip in (self.allowed_ips or '').split(',') if ip.strip()]
        return not ips or remote_addr in ips

    def _get_tz_selection(self):
        return [(tz, tz) for tz in sorted(pytz.all_timezones)]

    def action_sync_datetime(self):
        """Encola un comando ADMS para forzar la fecha/hora local del equipo.
        Se envía en el cuerpo de la respuesta de /iclock/getrequest la
        próxima vez que el equipo haga polling (normalmente segundos, si
        está en modo Realtime)."""
        Command = self.env['zk.device.command']
        for device in self:
            try:
                tz = pytz.timezone(device.tz or 'America/Mexico_City')
            except Exception:
                tz = pytz.timezone('America/Mexico_City')
            utc_now = datetime.now(pytz.UTC)
            local_now = utc_now.astimezone(tz).replace(tzinfo=None)
            Command.create({
                'device_id': device.id,
                'command': 'SET OPTIONS DateTime=%s' % local_now.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return True
