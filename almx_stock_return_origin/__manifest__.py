# -*- coding: utf-8 -*-
{
    'name': 'ALMX Stock Return Origin',
    'version': '19.0.1.1.0',
    'summary': 'Hace que las devoluciones regresen a la ubicación real de picking (Almacén 2/3, etc.) en vez de detenerse en la ubicación intermedia de entregas (Almacén 1).',
    'description': """
ALMX Stock Return Origin
=========================

Changelog
----------
- 19.0.1.1.0: Port a Odoo 19, reescrito sobre el wizard de 19.
  - En 19 _prepare_move_default_values vive en la LÍNEA del wizard
    (stock.return.picking.line) y la reserva ya no está separada de la
    cantidad, así que el destino se fija en los valores con los que se
    crea el move -- no hace falta deshacer reservas ni usar _split.
  - Multi-origen: en vez de repartir proporcionalmente (en 16 podía dar
    fracciones, p. ej. 0.4 pz), se llena primero la ubicación de donde
    salió más, hasta lo que salió de ahí, y luego la siguiente. Cada
    ubicación queda como su propio movimiento dentro de la devolución.
  - Encabezado del traslado: se fija ANTES de crear los moves (en 19
    escribir location_dest_id del picking reescribe el de todos sus moves).
    Si todo va a una sola ubicación se usa esa; si son varias, su
    ubicación padre común (si es interna); si no, el default de Odoo.
  - qty_done -> quantity.
- 16.0.1.0.4: Corrige que la lista/kanban de devoluciones mostrara
  "Customers -> Customers" (como si diera vueltas en círculo) aunque el
  movimiento real ya fuera a Almacén 2/3 correctamente. Causa: el
  wizard nativo crea el picking con self.picking_id.copy(...), que
  hereda location_dest_id del picking ORIGINAL (el OUT, destino
  Customers) en vez de reflejar el destino real de sus propios moves.
  Ahora se sincroniza location_dest_id del picking con el de su move
  (el de mayor cantidad si hay varios) justo después de resolver el
  origen, para que listas y kanban muestren la ruta real.
- 16.0.1.0.3: Corrige que la ubicación seguía cayendo en Almacén 1 en
  "Operaciones detalladas" a pesar del fix anterior. Causa: el
  _create_returns() nativo de Odoo llama internamente a
  new_picking.action_confirm() + new_picking.action_assign() DENTRO de
  sí mismo -- es decir, Odoo ya reserva y crea la línea real del move
  ANTES de que el código que corre después de super() (como
  _almx_apply_pick_origin) tuviera oportunidad de actuar. Cambiar
  location_dest_id del move después de ese punto no servía de nada: la
  línea ya había sido creada con el destino por defecto (Almacén 1) y
  no se actualiza retroactivamente. Ahora el destino correcto se
  decide en _prepare_move_default_values, con los valores con los que
  se CREA el move -- antes de cualquier action_confirm/action_assign
  -- para que la línea real nazca ya en la ubicación correcta. El caso
  de más de una ubicación de origen (poco común) se resuelve aparte,
  deshaciendo la reserva primaria y repartiendo con _split.
- 16.0.1.0.2: Corrige que la devolución igual terminaba en Almacén 1 (el
  destino por defecto) en vez de la ubicación real de origen del PICK,
  a pesar de que el módulo sí encontraba correctamente esa ubicación.
  La causa: _almx_apply_pick_origin creaba el stock.move.line con
  reserved_uom_qty ya puesto usando create(), pero el create() de
  stock.move.line NO reserva el quant real (esa lógica solo corre en
  el override de write()). La línea quedaba "reservada" solo en
  apariencia, sin respaldo en el quant, y Odoo la descartaba al
  comprobar disponibilidad/validar, resolviendo la reserva por su
  cuenta contra el destino por defecto del move. Ahora se redirige
  location_dest_id del propio move (o de cada sub-move vía _split, si
  el origen viene de más de una ubicación) ANTES de reservar, dejando
  que _action_assign nativo cree la línea real con la reserva de quant
  correcta -- el mismo mecanismo que usa el wizard nativo de Odoo
  cuando se indica una ubicación de destino manualmente.
- 16.0.1.0.1: Corrige un bug encontrado en producción: si el PICK original
  de una OUT antigua salió de una ubicación que desde entonces fue
  archivada/renombrada (p. ej. una ubicación vieja "Stock Doppler (obs.)"
  reemplazada por "Stock
  Doppler"), el módulo regresaba la devolución a esa ubicación archivada.
  El movimiento era válido, pero al estar en una ubicación inactiva no se
  reflejaba en los reportes normales de entradas/salidas del producto.
  Ahora se descartan las ubicaciones archivadas como destino y se cae al
  comportamiento por defecto (destino del tipo de operación, p. ej.
  Almacén 1) en esos casos.
- 16.0.1.0.0: Versión inicial.

Problema que resuelve
----------------------
En el flujo de dos pasos (Recogida -> Órdenes de entrega), el asistente de
devolución estándar de Odoo (`stock.return.picking`) solo conoce la ubicación
de origen del movimiento inmediato que se está devolviendo. Para una OUT esa
ubicación es "Almacén 1" (la zona de entregas/staging), NO la ubicación real
del almacén (Almacén 2, Almacén 3, etc.) de donde salió físicamente el
producto durante el Recogida (PICK).

Esto provoca que, por defecto, las devoluciones de mercancía queden
registradas en Almacén 1 en lugar de en su ubicación real de origen, y en la
práctica el personal terminaba escogiendo manualmente ubicaciones arbitrarias
(Almacén 2 o 3) sin ningún criterio, dejando el inventario inconsistente.

Qué hace este módulo
---------------------
Al confirmar una devolución, este módulo:

1. Ubica el movimiento de Recogida (PICK) original vinculado vía
   `move_orig_ids` al movimiento que se está devolviendo.
2. Lee las líneas de movimiento (`stock.move.line`) YA HECHAS de ese PICK,
   que sí conservan la ubicación física real de donde se tomó el producto.
3. Reparte la cantidad devuelta hacia esa(s) ubicación(es) real(es): si
   el PICK se abasteció de más de un sub-almacén, llena primero el de
   mayor cantidad (hasta lo que salió de ahí) y luego el siguiente.
4. Si no encuentra un PICK de origen (p. ej. devoluciones de compras u otros
   flujos sin este patrón), conserva el comportamiento estándar de Odoo sin
   modificarlo.

Alcance / limitaciones conocidas
---------------------------------
- Pensado para el patrón de 2 pasos (Recogida + Órdenes de entrega) usado en
  Doppler Elevadores S.A. de C.V. Si en el futuro se agregan más pasos
  intermedios (p. ej. un Empaque entre Recogida y Envío), la búsqueda de
  origen debe extenderse recursivamente (ahora solo sube un nivel).
- Fija `location_dest_id` del `stock.move` al crearlo (y crea un move
  adicional por cada ubicación extra si el PICK se abasteció de varias);
  la asignación de líneas la sigue haciendo Odoo de forma nativa.
""",
    'author': 'Irving Sammer González Correa - Alamex',
    'category': 'Inventory',
    'depends': ['stock'],
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
