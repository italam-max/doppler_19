# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

import pytz
from werkzeug.http import http_date

from odoo import fields, http
from odoo.http import request

_logger = logging.getLogger(__name__)

TEXT_HEADERS = [('Content-Type', 'text/plain')]

# Zona horaria a usar cuando todavía no se identifica el equipo (SN
# desconocido) o como último respaldo si la zona configurada es inválida.
DEFAULT_TZ = 'America/Mexico_City'

# Códigos de "Status" típicos en la línea ATTLOG.
CHECK_IN_STATUS = {'0', '4'}
CHECK_OUT_STATUS = {'1', '5'}

# Una entrada abierta con más de estas horas se considera salida olvidada:
# se cierra sin horas (out_mode='technical') para no generar turnos de cientos
# de horas ni bloquear la entrada del día siguiente. En 16 esto dejó 241
# asistencias de más de 16 h (hasta 861 h) entre agosto y septiembre de 2026.
MAX_SHIFT_HOURS = 16


def _local_date_header(tz_name=None):
    """Construye el valor del header HTTP 'Date' usando la hora LOCAL del
    equipo, en vez de la hora UTC real del servidor.

    Las terminales ZKTeco en modo Cloud Server/ADMS sincronizan su reloj
    interno tomando el header 'Date' de la respuesta HTTP en cada
    comunicación con el servidor (handshake, subida de ATTLOG, polling de
    getrequest, etc.), pero el firmware toma esos dígitos tal cual como
    hora local — no hace la conversión de zona horaria que exige el
    estándar HTTP (que manda ese header siempre en GMT).

    Si dejamos que el framework genere el header por default (UTC real),
    el equipo termina desfasado por la diferencia de horas con México, y
    cualquier ajuste manual que se haga en el equipo se sobreescribe en
    la siguiente comunicación. Por eso lo generamos nosotros: mismos
    dígitos que espera ver el equipo, con el formato HTTP-date estándar.
    """
    try:
        tz = pytz.timezone(tz_name or DEFAULT_TZ)
    except Exception:
        tz = pytz.timezone(DEFAULT_TZ)
    local_naive = datetime.now(pytz.UTC).astimezone(tz).replace(tzinfo=None)
    return http_date(local_naive)


def _headers_for(device=None):
    tz_name = device.tz if device else None
    return TEXT_HEADERS + [('Date', _local_date_header(tz_name))]


class ZkAdmsController(http.Controller):
    """Implementa el subconjunto del protocolo ADMS/iClock que usan las
    terminales ZKTeco (F22 y similares) cuando se configuran en modo
    "Cloud Server". El equipo es siempre quien inicia la conexión hacia
    Odoo, por lo que no requiere IP pública ni puertos abiertos hacia él.
    """

    # ------------------------------------------------------------------
    # Handshake + subida de datos
    # ------------------------------------------------------------------
    @http.route('/iclock/cdata', type='http', auth='none',
                methods=['GET', 'POST'], csrf=False, save_session=False)
    def cdata(self, **kwargs):
        sn = kwargs.get('SN') or kwargs.get('sn')
        device = self._get_device(sn)
        if not device:
            _logger.warning('ZK ADMS: SN desconocido o inactivo: %s', sn)
            # Respondemos OK de cualquier forma para no generar reintentos
            # agresivos de un equipo que no nos interesa registrar.
            return request.make_response('OK', headers=_headers_for())

        device.sudo().write({'last_seen': fields.Datetime.now()})

        if request.httprequest.method == 'GET':
            if kwargs.get('options') == 'all':
                # Handshake inicial: el equipo pregunta su configuración.
                body = self._build_handshake_response(device)
                return request.make_response(body, headers=_headers_for(device))
            return request.make_response('OK', headers=_headers_for(device))

        # POST: el equipo está subiendo datos de una tabla.
        table = kwargs.get('table')
        raw = request.httprequest.get_data(as_text=True) or ''

        if table == 'ATTLOG':
            processed = self._process_attlog(device, raw)
            device.sudo().write({
                'last_attlog_stamp': kwargs.get('Stamp') or device.last_attlog_stamp,
            })
            return request.make_response('OK: %d' % processed, headers=_headers_for(device))

        # OPERLOG (altas de huella/tarjeta), etc. Se reconoce pero no se
        # procesa todavía; se puede extender más adelante si se requiere
        # sincronizar empleados/huellas desde el equipo.
        _logger.info('ZK ADMS: tabla no procesada "%s" de SN=%s', table, sn)
        return request.make_response('OK', headers=_headers_for(device))

    # ------------------------------------------------------------------
    # Polling de comandos pendientes
    # ------------------------------------------------------------------
    @http.route('/iclock/getrequest', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    def getrequest(self, **kwargs):
        # El equipo pregunta periódicamente si hay comandos por ejecutar
        # (ej. borrar registros, reiniciar, fijar fecha/hora). El header
        # Date en hora local se sigue mandando como defensa adicional por
        # si algún firmware sí lo respeta, pero el mecanismo confiable es
        # el body de esta respuesta: por eso se despachan aquí los
        # comandos pendientes de zk.device.command.
        sn = kwargs.get('SN') or kwargs.get('sn')
        device = self._get_device(sn)
        if device:
            body = self._dispatch_commands(device)
            if body:
                _logger.info('ZK ADMS: enviando comando(s) a SN=%s:\n%s', sn, body)
                return request.make_response(body, headers=_headers_for(device))
        return request.make_response('OK', headers=_headers_for(device))

    @http.route('/iclock/devicecmd', type='http', auth='none',
                methods=['POST'], csrf=False, save_session=False)
    def devicecmd(self, **kwargs):
        sn = kwargs.get('SN') or kwargs.get('sn')
        device = self._get_device(sn)
        raw = request.httprequest.get_data(as_text=True) or ''
        # Se deja el log completo SIEMPRE (no solo cuando hay comandos
        # pendientes) porque todavía no está confirmado el formato exacto
        # que usa este firmware para acusar recibo. La primera vez que se
        # envíe un comando real, este log es lo que hay que revisar.
        _logger.info('ZK ADMS devicecmd SN=%s kwargs=%s raw_body=%r', sn, kwargs, raw)
        if device:
            self._ack_commands(device, kwargs, raw)
        return request.make_response('OK', headers=_headers_for(device))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_device(self, sn):
        if not sn:
            return None
        device = request.env['zk.device'].sudo().search(
            [('serial_number', '=', sn), ('active', '=', True)], limit=1)
        if device:
            remote_addr = request.httprequest.remote_addr
            if not device._almx_ip_allowed(remote_addr):
                _logger.warning('ZK ADMS: SN=%s rechazado, IP %s no permitida', sn, remote_addr)
                return None
        return device

    def _dispatch_commands(self, device):
        """Arma el body de respuesta con los comandos pendientes de este
        equipo (protocolo ADMS: una línea por comando, formato
        "C:<seq>:<comando>"), y los marca como enviados. Devuelve None si
        no hay nada pendiente (para que el caller regrese el 'OK' normal).

        Se limita a 5 por ciclo para no saturar un solo polling; si hay
        más, se van mandando en los siguientes ciclos (que en modo
        Realtime son cuestión de segundos).
        """
        Command = request.env['zk.device.command'].sudo()
        pending = Command.search([
            ('device_id', '=', device.id), ('state', '=', 'pending'),
        ], order='create_date asc', limit=5)
        if not pending:
            return None

        seq = device.cmd_seq_counter
        now = fields.Datetime.now()
        lines = []
        for cmd in pending:
            seq += 1
            cmd.write({'seq': seq, 'state': 'sent', 'sent_date': now})
            lines.append('C:%d:%s' % (seq, cmd.command))
        device.write({'cmd_seq_counter': seq})
        return '\n'.join(lines) + '\n'

    def _ack_commands(self, device, kwargs, raw):
        """Intenta casar la confirmación que manda el equipo (vía
        /iclock/devicecmd) con los comandos que le enviamos, usando el
        número de secuencia (seq/ID). El formato exacto de confirmación
        varía entre firmwares de ZKTeco, así que se intentan los patrones
        más comunes; si ninguno aplica, el detalle queda de cualquier
        forma en el log (ver devicecmd) para poder ajustar el parseo con
        datos reales."""
        Command = request.env['zk.device.command'].sudo()
        for seq, ok, raw_line in self._parse_cmd_acks(kwargs, raw):
            cmd = Command.search([
                ('device_id', '=', device.id), ('seq', '=', seq),
            ], limit=1)
            if not cmd:
                continue
            cmd.write({
                'state': 'done' if ok else 'error',
                'ack_date': fields.Datetime.now(),
                'raw_ack': raw_line,
            })

    def _parse_cmd_acks(self, kwargs, raw):
        """Devuelve una lista de tuplas (seq, ok, raw_line) a partir de la
        confirmación del equipo. Cubre los dos patrones más citados en
        implementaciones ADMS de referencia:

        1) Parámetros sueltos: ID=<seq>&Return=<0|codigo_error>
        2) Líneas en el cuerpo con el mismo patrón, una por comando
           confirmado (cuando el equipo acusa varios a la vez).

        Si tu equipo usa otro formato, este es el punto exacto a ajustar
        una vez que veamos el log real de devicecmd.
        """
        results = []

        cmd_id = kwargs.get('ID') or kwargs.get('CmdId') or kwargs.get('cmdid')
        if cmd_id is not None:
            try:
                seq = int(cmd_id)
            except (TypeError, ValueError):
                seq = None
            if seq is not None:
                ret = kwargs.get('Return', kwargs.get('return', kwargs.get('Ret')))
                ok = ret is None or str(ret) in ('0', 'OK')
                results.append((seq, ok, 'kwargs=%s raw=%r' % (kwargs, raw)))
                return results

        for line in raw.splitlines():
            line = line.strip()
            if not line or '=' not in line:
                continue
            try:
                pairs = dict(p.split('=', 1) for p in line.split('&') if '=' in p)
            except ValueError:
                continue
            if 'ID' not in pairs:
                continue
            try:
                seq = int(pairs['ID'])
            except ValueError:
                continue
            ret = pairs.get('Return')
            ok = ret is None or ret == '0'
            results.append((seq, ok, line))

        return results

    def _build_handshake_response(self, device):
        # Realtime=1 le indica al equipo que empuje cada marcaje al
        # instante, en vez de esperar a TransTimes.
        lines = [
            'GET OPTION FROM: SN=%s' % device.serial_number,
            'ATTLOGStamp=%s' % (device.last_attlog_stamp or 'None'),
            'OPERLOGStamp=None',
            'ErrorDelay=30',
            'Delay=10',
            'TransTimes=00:00;14:05',
            'TransInterval=1',
            'TransFlag=1111000000',
            'Realtime=1',
            'Encrypt=None',
            # EXPERIMENTAL: se observó que el equipo muestra su hora local
            # ~8h adelantada de la UTC real (posible default de fábrica
            # China, UTC+8). No hay confirmación de que este firmware
            # respete esta clave del handshake ADMS; se agrega para
            # descartarlo/confirmarlo con una prueba real (requiere que el
            # equipo se reinicie para volver a pedir esta configuración).
            'TimeZone=%s' % self._utc_offset_hours(device),
        ]
        return '\n'.join(lines) + '\n'

    def _utc_offset_hours(self, device):
        try:
            tz = pytz.timezone(device.tz or DEFAULT_TZ)
        except Exception:
            tz = pytz.timezone(DEFAULT_TZ)
        offset = datetime.now(pytz.UTC).astimezone(tz).utcoffset()
        hours = offset.total_seconds() / 3600
        # Formato entero si es exacto (ej. "-6"), decimal si no (ej. "5.5").
        if hours == int(hours):
            return str(int(hours))
        return str(hours)

    def _process_attlog(self, device, raw):
        Attendance = request.env['hr.attendance'].sudo()
        Employee = request.env['hr.employee'].sudo()
        try:
            tz = pytz.timezone(device.tz or 'America/Mexico_City')
        except Exception:
            tz = pytz.UTC

        count = 0
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) < 3:
                continue

            pin, ts_raw, status = parts[0].strip(), parts[1].strip(), parts[2].strip()

            try:
                local_dt = tz.localize(datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S'))
                ts_utc = local_dt.astimezone(pytz.UTC).replace(tzinfo=None)
            except ValueError:
                _logger.warning('ZK ADMS: timestamp no reconocido "%s" (línea: "%s")', ts_raw, line)
                continue

            employee = Employee.search([('zk_pin', '=', pin)], limit=1)
            if not employee:
                _logger.warning('ZK ADMS: PIN sin empleado asociado: %s (SN=%s)', pin, device.serial_number)
                continue

            try:
                if self._apply_punch(Attendance, employee, ts_utc, status):
                    count += 1
            except Exception:
                _logger.exception(
                    'ZK ADMS: error procesando marca de %s (PIN %s)', employee.name, pin)

        return count

    def _apply_punch(self, Attendance, employee, ts_utc, status):
        """Aplica una marca a hr.attendance. Devuelve True si generó/actualizó
        un registro, False si se descartó (duplicado, fuera de orden, etc.)."""

        # Evita duplicados exactos si el equipo reenvía la misma marca
        # (comportamiento normal de ADMS ante fallas de red).
        existing = Attendance.search([
            ('employee_id', '=', employee.id),
            ('check_in', '=', ts_utc),
        ], limit=1)
        if existing:
            return False

        open_attendance = Attendance.search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False),
        ], limit=1, order='check_in desc')

        if open_attendance and ts_utc - open_attendance.check_in > timedelta(hours=MAX_SHIFT_HOURS):
            _logger.warning(
                'ZK ADMS: %s tenía una entrada abierta desde %s (salida olvidada); '
                'se cierra sin horas antes de aplicar la marca %s',
                employee.name, open_attendance.check_in, ts_utc)
            open_attendance.write({'check_out': open_attendance.check_in, 'out_mode': 'technical'})
            open_attendance = Attendance.browse()

        is_checkout = status in CHECK_OUT_STATUS
        is_checkin = status in CHECK_IN_STATUS

        if is_checkout or (not is_checkin and open_attendance):
            # Marca de salida, o estado ambiguo con una entrada ya abierta:
            # se usa alternancia (toggle) como respaldo.
            if open_attendance and ts_utc > open_attendance.check_in:
                open_attendance.write({'check_out': ts_utc, 'out_mode': 'kiosk'})
                return True
            return False

        # Marca de entrada (o estado ambiguo sin entrada abierta).
        if not open_attendance:
            Attendance.create({'employee_id': employee.id, 'check_in': ts_utc, 'in_mode': 'kiosk'})
            return True
        return False
