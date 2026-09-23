{
    'name': 'ALMX - Candados de Movimientos de Inventario',
    'version': '19.0.1.1.0',
    'summary': 'Todo movimiento con documento: SO en PICK/OUT, PO o devolución en IN, '
               'Dirección para Merma/Laboratorio/Desecho, asignaciones solo TI/RH',
    'description': """
        Objetivo: evitar pérdida de stock cerrando todas las entradas y salidas
        que no estén respaldadas por un documento.

        1. PICK / OUT (tipos con "Requiere Pedido de venta"):
           - "Pedido de venta" pasa al encabezado y es obligatorio; "Documento
             origen" baja a Información adicional y se llena solo con la SO.
           - Solo SO confirmadas y de la misma compañía.
           - Al elegir la SO se llenan cliente, dirección de entrega y origen.
           - Al validar, se bloquea si no hay SO confirmada ligada (excepto
             devoluciones nativas, p. ej. devolución a proveedor).
        2. IN (tipos con "Candado de recepciones"):
           - Válido si viene de una Orden de compra o es una devolución nativa
             (botón Devolver). Cualquier otro IN solo lo valida Dirección.
        3. Ubicaciones con "Requiere autorización de Dirección" (Merma,
           Laboratorio, Desecho): cualquier traslado con destino ahí (o en una
           sububicación, revisado línea por línea) solo lo valida Dirección.
           Validar = autorizar. Botón "Solicitar autorización" para avisarles.
        4. Botón Desechar (stock.scrap): solo Dirección.
        5. Tipos de operación de "Asignación de equipo" (EPP, celulares,
           equipo): solo los usa el grupo de Asignación (TI y RH) y solo hacia
           ubicaciones marcadas como "Ubicación de asignación". Sin aprobación.

        6. Congelado de contenido (tipos con "Congelar contenido", pensado
           para OUT): una vez confirmado no se agregan/quitan líneas, ni se
           cambia producto o cantidad pedida, ni se entrega más de lo pedido
           (entregar menos sí: backorder por falta de stock). La SO
           confirmada también queda congelada para artículos de inventario.
           Si el pedido está mal: cancelar la SO y hacer otra. El PICK sigue
           abierto (Laboratorio agrega material de controles, como en 16).

        Sustituye a los prototipos de 16 almx_delivery_sale_guard y
        almx_internal_transfer_guard (nunca llegaron a producción) y a
        stock_freeze_lines de 16 (que solo congelaba agregar/borrar líneas en OUT).

        Changelog
        - 19.0.1.1.0: congelado de contenido en OUT y SO confirmada.
        - 19.0.1.0.0: versión inicial.
    """,
    'author': 'Irving Sammer González Correa - Alamex',
    'category': 'Inventory/Inventory',
    'depends': ['stock', 'sale_stock', 'purchase_stock', 'mail', 'almx_stock'],
    'data': [
        'security/security.xml',
        'views/stock_location_views.xml',
        'views/stock_picking_type_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
