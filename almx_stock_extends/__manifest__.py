# -*- coding: utf-8 -*-
{
    'name': "almx_stock_extends",

    'summary': """
        Módulo para relacionar los picks y outs""",

    'description': """
Este módulo relaciona de manera automatica los picks y outs con un campo readonly cuando son creados por el sistema.
Cuando son creados manualmente, se crea un campo many2one para que se pueda seleccionar el el pick u out correspondiente.

Changelog
----------
- 16.0.1.0.11: A petición explícita (se prefiere inmediato sobre
  esperar al cron): se agrega el enlace INMEDIATO real de
  related_pick_id/related_out_id, en StockMove.write() -- reaccionando
  al momento exacto en que el motor de aprovisionamiento le asigna
  'picking_id' a un move recién creado (el mismo instante en que,
  del lado del picking, 'group_id' pasa a tener valor real). El cron
  de la 16.0.1.0.10 se conserva, pero ahora solo como red de
  seguridad -- no como mecanismo principal.

  Se decidió no hacer esto desde el principio por ser stock.move un
  modelo de tráfico mucho más alto que stock.picking (cada reserva,
  cada cambio de cantidad pasa por su write()); se mitiga con un guard
  de 'picking_id' in vals como PRIMERA condición (costo casi nulo en el
  resto de los writes) y con try/except (un fallo aquí nunca debe
  tumbar la asignación real del move a su picking). Reutiliza tal cual
  _almx_autolink_related_ids_from_group y _almx_autolink_related_moves,
  sin duplicar lógica.
- 16.0.1.0.10: CORRECCIÓN de la 16.0.1.0.9, encontrada al verificar en
  vivo contra un PICK/OUT de prueba recién creados (nunca llegó a
  funcionar para el caso automático real, aunque no rompió nada):

  1. El create() de la 16.0.1.0.9 llamaba a
     _almx_autolink_related_ids_from_group() usando los campos
     pick_move/out_move para identificar PICK/OUT. Esos dos campos NO
     tienen `compute=` en su propia declaración -- Odoo solo los
     recalcula como efecto secundario de compute_picking_type_move,
     que a su vez solo se dispara cuando algo lee 'detect_move_type'.
     Un picking recién creado que nadie ha abierto trae pick_move/
     out_move en False sin importar su tipo de operación real. Se
     corrige leyendo picking_type_id.sequence_code directamente, que no
     depende de que otro campo lo haya disparado antes.

  2. Aun con eso corregido, hacerlo en create() no funciona para el
     caso que importa: 'group_id' es un related field a
     move_ids.group_id, y en el flujo nativo de Odoo el picking se crea
     VACÍO -- los movimientos se le asignan después, con un write() de
     picking_id sobre cada move, ya en otro paso del motor de
     aprovisionamiento. O sea que dentro del propio create() del
     picking, group_id casi nunca está disponible todavía. Se cambia el
     disparador de create() a un cron
     (_cron_almx_autolink_related_ids, cada 10 min, ver
     data/almx_cron.xml) que revisa lo creado en los últimos 7 días --
     para cuando corre, el motor de aprovisionamiento ya terminó y
     group_id/move_ids ya están completos. create() se deja tal como
     estaba antes de la 16.0.1.0.9 (solo _almx_autolink_related_moves).
- 16.0.1.0.9: related_pick_id/related_out_id ahora también se enlazan
  cuando el PICK y el OUT los genera automáticamente el motor de
  aprovisionamiento nativo de Odoo (al confirmar una orden de venta --
  así se crea la mayoría de los pares, y hasta ahora nada llenaba estos
  campos para ese caso; solo se llenaban con el botón "Crear OUT"/
  "Crear INT" o a mano). Se agrega _almx_autolink_related_ids_from_group,
  llamado desde create(): empareja PICK y OUT por 'group_id' (el grupo
  de aprovisionamiento, único por orden) SOLO cuando ambos existen ya
  y son exactamente uno de cada tipo -- si hay más de un PICK o más de
  un OUT en el mismo grupo (backorders, entregas parciales), no adivina.

  OJO: un enfoque similar (emparejar por group_id) ya se había
  intentado antes en relational_moves() y se revirtió en la 16.0.1.0.7
  por un bug real -- buscaba con [('group_id','=', False)], y como los
  traslados manuales casi nunca tienen group_id, cualquier picking sin
  grupo de CUALQUIER otra orden calificaba, pisando el enlace correcto
  con uno equivocado. Este método es distinto en ese punto exacto:
  jamás actúa sobre group_id vacío/False, solo sobre un valor real y
  específico. Una vez enlazados los related_*_id, el enlace nativo
  move_orig_ids/move_dest_ids se dispara solo (ya lo hace
  _almx_autolink_related_moves, sin cambios, desde la 16.0.1.0.7).

  Alcance: igual que el resto del módulo, identifica PICK/OUT por
  picking_type_id.sequence_code ('NWH/PICK/', 'NWH/OUT/') -- por ahora
  solo cubre el almacén NWH.
- 16.0.1.0.8: HOTFIX urgente -- la 16.0.1.0.7 rompía la creación manual
  de OUT/INT cuando el formulario guarda el encabezado y las líneas de
  movimiento en un solo create() (el flujo normal de "Nuevo" traslado).
  Error: psycopg2.ProgrammingError: can't adapt type 'NewId'.

  Causa: al procesar move_ids_without_package, Odoo internamente
  reescribe move_ids como parte del mismo create() -- y 'move_ids'
  estaba en la lista de campos que disparaban el enlace automático
  agregado en 16.0.1.0.7. Ese enlace se re-disparaba en ese punto
  intermedio, cuando los stock.move recién creados todavía tenían un
  NewId (marcador interno de Odoo para records aún no insertados en la
  base), no un id real -- y psycopg2 no sabe convertir un NewId a SQL.

  Corrección: se quita 'move_ids' de los campos que disparan el enlace
  automático (ese write interno de Odoo ya no lo dispara; el propio
  create() de este módulo sigue disparándolo explícitamente después de
  que super().create() termina, momento en el que los ids ya son
  reales). Además se agregó un guard defensivo en
  _almx_sync_pick_out_move_chain que verifica que ningún move
  involucrado sea todavía un NewId antes de escribir move_orig_ids/
  move_dest_ids, como red de seguridad adicional ante otros módulos
  (se detectó doppler/stock_picking_fix en la pila de este error, no
  visible desde esta sesión) que puedan disparar el mismo camino desde
  otro punto.
- 16.0.1.0.7: Blindaje del enlace PICK/OUT manual, para casos donde el
  par no se crea con el botón "Crear OUT"/"Crear INT" (traslado creado a
  mano o duplicado, llenando related_pick_id/related_out_id
  directamente en el formulario). En esos casos el enlace nativo
  move_orig_ids/move_dest_ids nunca se ejecutaba, y el OUT podía perder
  ante otra orden la existencia que su propio PICK acababa de generar.
  Ahora stock.picking reproduce ese mismo enlace (emparejando por
  producto, exigiendo que ambos traslados compartan 'origin') cada vez
  que se guarda un traslado con related_pick_id/related_out_id o con
  líneas nuevas -- sin importar si se usó el botón o no.

  De paso se corrige un bug de mayor riesgo en relational_moves()
  (sale.order.is_related): al no tener @api.depends, ese compute corre
  cada vez que se abre el formulario del pedido de venta (el campo está
  visible ahí), y buscaba PICK/OUT por 'group_id' -- campo que los
  traslados manuales casi nunca tienen, por lo que el filtro podía
  devolver traslados de OTRAS órdenes de venta sin relación alguna y
  sobrescribir related_pick_id/related_out_id con el par equivocado cada
  vez que alguien abría el pedido. Ahora ese compute solo calcula el
  indicador informativo is_related, sin tocar related_pick_id/
  related_out_id de ningún registro.
- 16.0.1.0.6: Se agrega visibilidad de devoluciones en el propio
  documento (PICK/OUT/INT): un smart button "Devoluciones" (contador,
  incluye canceladas) que abre la(s) devolución(es) generada(s) a
  partir de sus movimientos, y una columna "Devuelto" en cada línea de
  producto (pestaña Operaciones) mostrando cuánto de esa línea
  específica ya se devolvió (solo cuenta devoluciones en estado done).
  Antes no había ninguna forma de saber, desde el documento original,
  si hubo una devolución ni para qué producto -- había que adivinar el
  nombre de la devolución o buscarla a mano.
- 16.0.1.0.5: Corrige que "Comprobar disponibilidad" no reservaba nada
  en los OUT generados por action_create_related_out a partir de un
  PICK manual. El move nuevo se creaba con location_id = origen del
  move del PICK (p. ej. Stock Doppler), en vez de su destino (donde
  realmente quedó la mercancía, p. ej. Almacén 1). El picking en sí ya
  tenía el location_id correcto desde la 16.0.1.0.1 -- faltaba
  replicar el mismo criterio a nivel de move. Ahora el move usa
  picking_out.location_id (ya calculado correctamente) en vez de
  copiar move.location_id del PICK original.
- 16.0.1.0.4: Corrige IndexError: list index out of range al llamar
  action_almx_assign_manual_out_creators desde el <function> de
  security_groups.xml. Sin @api.model, Odoo despacha ese método como
  método de instancia y espera que el primer argumento sea una lista de
  ids para hacer .browse() -- como el <function> no pasa argumentos,
  args quedaba vacío. Se agrega @api.model para que el método se
  invoque directamente, sin requerir ids.
- 16.0.1.0.3: Corrige la asignación de usuarios del grupo "Alamex: Crear
  OUT manual (traslados)". La versión anterior intentaba resolverla con
  un eval de XML tipo obj().env[...].search(...), que no es válido en el
  sandbox de eval de Odoo (no expone el ORM completo) y tumbaba toda la
  actualización del módulo con NameError: name 'obj' is not defined.
  Ahora la búsqueda por login vive en un método Python real
  (res.groups.action_almx_assign_manual_out_creators), invocado desde
  security_groups.xml con una etiqueta <function>, que sí corre con el
  ORM completo tanto al instalar como en cada actualización del módulo.
- 16.0.1.0.2: Se agrega un grupo de seguridad nuevo
  ("Alamex: Crear OUT manual (traslados)") y se restringe el botón
  "Crear OUT" a un conjunto específico de personas (Diego, Yazan,
  Hamdi, Celia, Alexis, Irving, César Iván) en vez del grupo
  genérico de Inventario. Los usuarios se buscan por correo al
  instalar/actualizar el módulo, para que la asignación se
  restaure sola si el módulo se reinstala. El botón "Crear INT"
  no se tocó -- sigue con el grupo de Inventario general.
- 16.0.1.0.1: Corrige que el botón "Crear OUT" (action_create_related_out)
  nunca llenaba los campos related_out_id/related_pick_id que este mismo
  módulo ya define para relacionar visualmente el PICK y el OUT -- quedaban
  siempre vacíos. Tampoco establecía el enlace nativo de Odoo
  (move_orig_ids/move_dest_ids) entre los movimientos del PICK y el OUT
  generado, lo cual rompía la trazabilidad nativa (necesaria, entre otras
  cosas, para que las devoluciones sepan a qué ubicación regresar la
  mercancía). Además, el OUT generado quedaba con las ubicaciones
  incorrectas: heredaba tal cual la ubicación de destino del PICK como su
  propio origen Y destino (Almacén -> mismo Almacén), en vez de
  Almacén -> Cliente. Ahora action_create_related_out realiza lo siguiente:

  1. Calcula correctamente el origen (destino del PICK) y destino
     (ubicación del cliente, o el destino por defecto del tipo de
     operación OUT) del nuevo traslado.
  2. Enlaza move_orig_ids/move_dest_ids entre cada movimiento del PICK
     y su correspondiente movimiento nuevo en el OUT.
  3. Llena related_out_id / related_pick_id automáticamente.

  action_create_related_int (botón "Crear INT") recibió el mismo fix de
  enlace (move_orig_ids/move_dest_ids y related_*_id), pero NO se tocaron
  sus ubicaciones -- pendiente de confirmar cuál es el comportamiento de
  negocio esperado ahí antes de replicar ese cambio.
    """,

    'author': "Celia y Jorge",
    'website': "www.alam.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '19.0.1.0.12',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale','almx_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security_groups.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/stock_view.xml',
        'views/sale_view.xml',
        'data/almx_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
