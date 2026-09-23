# -*- coding: utf-8 -*-
{
    'name': 'ALMX Serial Verification on Validate',
    'version': '19.0.1.1.0',
    'summary': 'Al validar un traslado, pide capturar manualmente el número de serie a entregar y lo verifica contra los números de serie dados de alta antes de proceder.',
    'description': """
ALMX Serial Verification on Validate
=======================================

Changelog
----------
- 19.0.1.1.0: Port a Odoo 19.
  - qty_done / reserved_uom_qty -> quantity + picked (modelo de 19). Al
    confirmar se escribe el número de serie y se marca la línea "picked".
  - En 19 el número reservado ya no se ve en lot_id sino en el selector
    de quant ("Recoger de": ubicación/serie/paquete) y en la columna
    opcional de series del movimiento. Se ocultan ambos en líneas de
    producto con serie cuando el tipo de operación exige confirmación, y
    se agrega columna de solo lectura con la ubicación de origen para
    no perderla.
  - Verificación de disponibilidad: se busca el quant de ESA serie dentro
    de la ubicación origen del movimiento (incluye sububicaciones) y, si
    está en otra sububicación distinta a la reservada, se reubica la
    línea ahí. En 16 solo se aceptaba si estaba en la misma ubicación
    exacta de la línea.
  - La búsqueda de la serie respeta la compañía del traslado.
  - Solo se evalúan los movimientos que Odoo 19 va a procesar (si hay
    alguno marcado como "picked", solo esos).
  - Vistas: attrs -> expresiones de 19, tree -> list.
- 16.0.1.0.3: Corrige dos bugs encontrados en pruebas en vivo:
  1. El wizard nunca marcaba la cantidad como "Hecho" (`qty_done`) en la
     línea real antes de validar -- solo corregía el número de serie. Esto
     dejaba el traslado esperando cantidades y nunca se completaba solo.
     Ahora se marca automáticamente al confirmar.
  2. Si el operador escribía exactamente el mismo número de serie que
     Odoo ya había reservado automáticamente para esa línea, el sistema
     lo rechazaba como "no disponible" -- porque la verificación de
     disponibilidad restaba la propia reserva de la línea sin darse
     cuenta de que era su propia reserva. Ahora, si el número coincide
     con el ya reservado por la misma línea, se acepta de inmediato.
- 16.0.1.0.2: Corrige un bug real de sincronización: el botón "Confirmar y
  validar" confiaba en el campo `is_valid` calculado por el onchange del
  navegador, el cual no siempre se guardaba antes de ejecutar el botón
  (dependía del comportamiento de guardado de la vista de lista
  editable). Ahora la validez se vuelve a calcular de forma autoritativa,
  server-side, directamente a partir de `entered_serial` en el momento de
  confirmar -- ya no depende de ningún campo calculado previamente.
- 16.0.1.0.1: Corrige permisos de acceso del wizard (quedan globales, sin
  requerir grupo específico, en vez del grupo Employee usado por error en
  la 16.0.1.0.0). Añade ocultamiento del número de serie pre-reservado en
  la pestaña "Operaciones detalladas", pero SOLO para líneas cuyo producto
  tiene seguimiento por número de serie (no afecta productos de lote/batch
  ni productos sin seguimiento, aunque compartan traslado con uno de
  serie).
- 16.0.1.0.0: Versión inicial.

Problema que resuelve
----------------------
Para productos con seguimiento por número de serie, Odoo reserva
automáticamente un número de serie específico en cuanto se confirma el
pedido de venta, ANTES de que cualquier persona haya tocado físicamente el
producto. Si el operador no verifica la etiqueta física y toma otra
unidad, el número registrado ya no coincide con lo realmente entregado.

Qué hace este módulo
---------------------
1. En Configuración > Tipos de operaciones, se añade la casilla
   "Requiere confirmación manual de número de serie". Se activa por tipo
   de operación (normalmente solo en "Recogida").
2. Al presionar "Validar" en un traslado de ese tipo que tenga productos
   con número de serie, en vez de validar directamente se abre una
   ventana pidiendo ingresar, para cada producto, el número de serie que
   se va a entregar (el campo empieza VACÍO, no se muestra el número que
   el sistema reservó automáticamente, precisamente para obligar a mirar
   la etiqueta física en vez de copiar lo que ya estaba puesto).
3. Al escribir el número, el sistema lo verifica en el momento contra los
   números de serie dados de alta para ese producto:
   - Si no existe -> "Número de serie no encontrado para este producto".
   - Si existe pero no hay existencia disponible en la ubicación de
     origen del movimiento -> mensaje indicando que no hay existencia ahí.
   - Si existe y hay existencia disponible -> "Número de serie válido".
4. Solo cuando TODAS las líneas quedan en "Número de serie válido" se
   habilita el botón "Confirmar y validar". Al presionar ese botón, el
   número de serie capturado se escribe en la línea de movimiento
   correspondiente (lo que hace que Odoo reacomode automáticamente la
   reserva, de forma nativa, si el número capturado es distinto al que se
   había reservado) y se completa la validación del traslado.
5. Además, en la pestaña "Operaciones detalladas" del propio traslado, se
   oculta el número de serie que Odoo reservó automáticamente -- solo
   para las líneas cuyo producto tiene seguimiento por número de serie en
   un tipo de operación con la confirmación activada. Así el operador no
   ve ningún número antes de llegar al wizard. La reserva interna sigue
   funcionando igual (la ubicación de origen del movimiento, como
   "Almacén 2", se sigue mostrando normalmente).

Qué NO hace (y por qué no hace falta)
---------------------------------------
No reimplementa el reacomodo de la reserva al escribir un número de serie
distinto al reservado: esa lógica ya existe de forma nativa en
`stock.move.line.write()`. Este módulo solo añade el paso de captura y
verificación manual antes de que ese cambio se aplique.

Alcance recomendado
---------------------
Activar la casilla en el tipo de operación "Recogida" (PICK) de Doppler
Elevadores S.A. de C.V., que es el paso donde el personal toma físicamente
el producto. La Órdenes de entrega (OUT) no necesita este paso: al
reservar desde Almacén 1 después de que el PICK ya quedó validado con el
número de serie correcto, el sistema toma automáticamente esa misma pieza
física.
""",
    'author': 'Irving Sammer González Correa',
    'category': 'Inventory',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_type_views.xml',
        'views/stock_move_line_views.xml',
        'wizard/serial_confirm_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
