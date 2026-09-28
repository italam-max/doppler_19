# almx_zkt_attendance

Integración en tiempo real de terminales ZKTeco (F22 y compatibles) con
`hr.attendance`, vía protocolo ADMS/push. El equipo se conecta hacia Odoo
por HTTPS saliente — no necesita IP pública ni puertos abiertos hacia él.

## 1. Configuración en el equipo F22

En el menú del equipo (la ruta exacta puede variar un poco según firmware):

`Menú > Comm > Cloud Server Setting` (a veces aparece como "ADMS")

- **Enable Server**: Sí / ON
- **Server Address**: `alam.mx` (o el dominio/IP donde publiques el módulo;
  recomendado probar primero en tu rama de staging de Odoo.sh)
- **Server Port**: `443` si usas HTTPS (recomendado), `80`/otro si HTTP
- **Enable Domain Name**: Sí, si usas un dominio en vez de IP
- **HTTPS**: Sí

Después de guardar, el equipo debería mostrar el estado de conexión como
"Conectado" o similar en unos segundos/minutos. Este es el momento del
*handshake* (`GET /iclock/cdata?...&options=all`).

El **número de serie (SN)** del equipo se consulta en
`Menú > Info del Sistema > Info del Dispositivo` o en `Comm > Ethernet`.

## 2. Configuración en Odoo

1. Instala el módulo (`almx_zkt_attendance`).
2. Ve a **Empleados > Configuración > Terminales ZKTeco** y crea un registro
   con el SN del equipo y su zona horaria real (importante si tienes
   plantas en distintos estados).
3. En la ficha de cada empleado, junto al campo "Badge ID", captura su
   **PIN checador ZKTeco** — debe coincidir exactamente con el número de
   enrolamiento que tiene en el equipo (el que usó para dar de alta su
   huella/tarjeta).
4. Sin este PIN, las marcas de ese empleado se descartan (se registran en
   el log de Odoo con advertencia, pero no rompen el resto del lote).

## 3. Prueba en vivo

1. Registra una marca de prueba en el equipo.
2. Revisa el log de Odoo (`grep "ZK ADMS"` en los logs del worker) para
   confirmar que llegó el POST a `/iclock/cdata` y se procesó.
3. Verifica que apareció el registro correspondiente en
   **Asistencias > Vista general**.

## 4. Sincronización de fecha/hora del equipo (v1.1.0 → v1.2.0)

**Síntoma que corrige:** el equipo "no ajusta" la fecha aunque la cambies
manualmente en el menú del dispositivo — en cuanto vuelve a comunicarse
con Odoo, regresa a una hora desfasada.

**Intento v1.1.0 (header `Date`) — descartado.** La hipótesis inicial fue
que la terminal sincroniza su reloj tomando el header HTTP `Date` de la
respuesta del servidor (comportamiento documentado en varias terminales
ZKTeco en modo Cloud Server/ADMS). Se intentó generar ese header con la
hora local en vez de la UTC real. En pruebas reales se confirmó que esto
**no funciona de forma confiable**: el servidor HTTP que usa Odoo
(Werkzeug, basado en `http.server.BaseHTTPRequestHandler` de Python)
manda su propio `Date` con la hora real del sistema automáticamente
*antes* de procesar los headers de la aplicación, y no lo reemplaza —
la respuesta cruda termina con dos líneas `Date:`, y la real es la que
prevalece camino al equipo. Esto no se puede corregir de forma confiable
desde el código de la aplicación sin parchar el servidor HTTP mismo.

**Solución v1.2.0 — canal de comandos ADMS (en el cuerpo, no en headers).**
El protocolo ADMS soporta mandarle comandos explícitos al equipo en el
*cuerpo* de la respuesta de `/iclock/getrequest` (que el equipo hace
polling constantemente, cada pocos segundos en modo Realtime), con el
formato `C:<id>:<comando>`. Se agregó:

- Modelo `zk.device.command`: cola/historial de comandos por terminal,
  con estado (`pending` → `sent` → `done`/`error`) y la respuesta cruda
  del equipo guardada tal cual.
- Botón **"Sincronizar fecha/hora en el equipo"** en la ficha de cada
  terminal (**Empleados > Configuración > Terminales ZKTeco**): encola
  un comando `SET OPTIONS DateTime=<hora local>` calculado con la zona
  horaria configurada en el registro.
- El equipo recoge el comando en su siguiente `getrequest`, y su
  confirmación (vía `/iclock/devicecmd`) se intenta casar automáticamente
  contra el comando pendiente.

**⚠️ Importante — la sintaxis exacta no está 100% confirmada.**
`SET OPTIONS DateTime=YYYY-MM-DD HH:MM:SS` es el formato más citado en
implementaciones ADMS de referencia, pero varía entre firmwares. Lo mismo
aplica al formato de confirmación que manda el equipo de vuelta (se
intentan los patrones `ID=<seq>&Return=<código>` más comunes). **Por
esto todo queda registrado sin importar si se reconoce o no:**
- El log del worker (`grep "ZK ADMS" `) siempre imprime el body completo
  que se le mandó al equipo, y el kwargs + cuerpo crudo completo de cada
  llamada a `/iclock/devicecmd`.
- Cada `zk.device.command` guarda su `raw_ack` tal cual llegó.

**Cómo probarlo en vivo:**
1. Ve a la ficha de la terminal y da clic en "Sincronizar fecha/hora en
   el equipo".
2. Revisa la pestaña "Comandos ADMS" del mismo registro: debe pasar de
   `Pendiente de envío` a `Enviado, esperando confirmación` en el
   siguiente polling del equipo.
3. Revisa físicamente en el equipo si la hora se corrigió.
4. Revisa el log del worker para ver exactamente qué se mandó y qué
   contestó el equipo — si el estado se queda en "Enviado" sin pasar a
   "Confirmado", lo más probable es que el equipo sí haya aplicado el
   comando pero con un formato de confirmación distinto al esperado; en
   ese caso el log trae el detalle crudo para ajustar `_parse_cmd_acks`
   en `controllers/main.py`.

## 5. Notas y pendientes recomendados antes de producción

- **Autenticación del equipo**: hoy la única validación es que el SN esté
  dado de alta y activo en `zk.device`. El endpoint es público por
  necesidad (el equipo no puede hacer OAuth). Si el firmware del F22
  soporta una "Comm Key"/clave de comunicación, vale la pena añadir esa
  validación al controlador como segunda capa.
- **Códigos de estado (`status`)**: se asumió la convención estándar
  ZKTeco (0/4 = entrada, 1/5 = salida), con alternancia como respaldo. Vale
  la pena confirmar con las primeras marcas reales de tu equipo qué valores
  manda exactamente y ajustar `CHECK_IN_STATUS`/`CHECK_OUT_STATUS` en
  `controllers/main.py` si hace falta.
- **Multi-planta**: si vas a conectar varias terminales (distintos
  almacenes/sucursales), cada una se registra como un `zk.device` separado
  con su propia zona horaria.
- **Multi-empresa**: la búsqueda de empleado por PIN no filtra por
  compañía todavía; agregar ese dominio si manejas PINs repetidos entre
  compañías distintas.
- **Comandos remotos**: `/iclock/getrequest` siempre responde "OK" (sin
  comandos). Si más adelante quieres, por ejemplo, forzar una
  resincronización o reinicio remoto, ahí es donde se implementaría.
