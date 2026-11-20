# almx_metodo_envio

Métodos de envío de Alamex: Paquetería, Flete, Entrega inmediata, Recolección programada,
Servicio de app y Proyecto Alamex.

- Cada método tiene una clasificación (almx_shipping_kind) que decide qué datos se piden en la venta.
- Los datos se validan al confirmar la venta (las cotizaciones en borrador no se bloquean).
- Tres Guerras y Castores exigen datos fiscales completos del cliente (RFC, razón social, régimen fiscal y CP).
- Proyecto Alamex solo aplica a ventas de Equipo Nuevo (sale_type = project).
- PICK y OUT muestran los datos leyéndolos de su venta (campos related, sin copia).
- Reemplaza la detección de recolección de almx_sale (comparaba el nombre del método) por la clasificación.
- Todo el flujo (ventanas, datos obligatorios y bloqueo de campos) aplica solo a ventas de Refacciones (sale_type = spare). En los demás tipos el método de envío se captura como antes.
