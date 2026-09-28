# Changelog — almx_zkt_attendance

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
El versionado sigue el esquema de Odoo (`16.0.MAYOR.MENOR.PARCHE`).

## [19.0.1.4.0]

### Cambiado (port a Odoo 19)
- `_sql_constraints` reemplazado por `models.Constraint` (en 19 ya no se aplica): PIN único por empleado y SN único por terminal.
- Vistas: `tree` → `list`, `attrs` → `invisible`; PIN del checador después del bloque de Badge ID.
- Checadas registradas con `in_mode`/`out_mode` = `kiosk` para distinguirlas de las manuales.
- `datetime.utcnow()` (deprecado en Python 3.12) → `datetime.now(pytz.UTC)`.

### Corregido
- Salida olvidada: una entrada abierta con más de 16 h se cierra sin horas (`out_mode='technical'`) antes de aplicar la siguiente marca. Antes la siguiente salida la cerraba (turnos de hasta 861 h) y la entrada del día se descartaba.

### Agregado
- `zk.device.allowed_ips`: lista opcional de IPs públicas permitidas por terminal. Vacío = sin restricción.

## [16.0.1.3.0]

### Experimental
- Se agrega `TimeZone=<offset>` (ej. `-6` para México) a la respuesta del
  handshake inicial (`GET /iclock/cdata?options=all`), calculado
  dinámicamente desde la zona horaria configurada en `zk.device`.
  **No confirmado si este firmware respeta esta clave** — se agrega para
  descartar/confirmar la hipótesis de que el desfase de +8h observado en
  el equipo viene de un default de zona horaria no configurado (posible
  default de fábrica China, UTC+8). Requiere que el equipo se reinicie
  para volver a solicitar esta configuración (el handshake normalmente
  solo se pide una vez por conexión/arranque, no en cada polling).
- Contexto: se confirmó en pruebas reales que el comando
  `SET OPTIONS DateTime=...` (canal de la v1.2.0) es aceptado por el
  equipo (`Return=0`) pero no tiene ningún efecto real sobre su reloj —
  esa clave específica no está soportada por este firmware para ese fin.
  El mecanismo confiable y documentado para fijar la hora de estos
  equipos es el protocolo nativo (TCP puerto 4370, comando `CMD_SET_TIME`,
  usado por librerías como `pyzk`), pero requiere acceso desde la misma
  red local del equipo — está en evaluación como plan alterno, bloqueado
  actualmente por una Comm Key desconocida en el equipo.

## [16.0.1.2.0]

### Cambiado
- Se descarta el enfoque de la v1.1.0 (header `Date` localizado):
  confirmado en pruebas reales que Werkzeug (servidor HTTP de Odoo)
  manda su propio header `Date` con la hora real del sistema de forma
  automática e irremplazable desde la aplicación.

### Agregado
- **Canal de comandos ADMS** para sincronizar fecha/hora (y a futuro,
  otros comandos remotos): nuevo modelo `zk.device.command`, botón
  "Sincronizar fecha/hora en el equipo" en la ficha de cada terminal,
  despacho de comandos pendientes vía el body de `/iclock/getrequest`,
  e intento de casar la confirmación del equipo vía `/iclock/devicecmd`.
  Logging exhaustivo (kwargs + body crudo) en cada llamada a
  `devicecmd` para poder ajustar el formato de confirmación con datos
  reales del firmware específico.

## [16.0.1.1.0]

### Corregido
- **Sincronización de fecha/hora del equipo.** Las terminales ZKTeco en
  modo Cloud Server/ADMS sincronizan su reloj interno tomando el header
  HTTP `Date` de la respuesta del servidor, pero el firmware no aplica
  la conversión de zona horaria (toma esos dígitos como hora local). Al
  dejar que el framework mandara la UTC real por default, el equipo
  quedaba desfasado frente a México y cualquier ajuste manual se
  sobreescribía en la siguiente comunicación.
  Ahora los endpoints `/iclock/cdata`, `/iclock/getrequest` y
  `/iclock/devicecmd` generan el header `Date` usando la hora local de
  la zona horaria configurada en cada `zk.device`, en vez de la UTC real.
  Detalle y pasos de verificación en `README.md`, sección 4.

## [16.0.1.0.0]

### Agregado
- Integración inicial ADMS/push con terminales ZKTeco (F22 y
  compatibles): endpoints `/iclock/cdata`, `/iclock/getrequest`,
  `/iclock/devicecmd`.
- Modelo `zk.device` (catálogo de terminales, número de serie, zona
  horaria, último contacto).
- Campo `zk_pin` en `hr.employee` para el PIN de enrolamiento.
- Procesamiento de tabla `ATTLOG` con detección de entrada/salida por
  código de estado y respaldo por alternancia (toggle).
