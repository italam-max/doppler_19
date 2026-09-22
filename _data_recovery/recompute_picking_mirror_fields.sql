-- Recalculo de campos espejo en stock.picking (sept 2026)
-- Correr DESPUES de recovery_sale_order.sql: la recuperacion por SQL de
-- sale_order.sale_type / completely_paid no dispara el recalculo de los
-- campos guardados que dependen de ellos en stock_picking.
-- Resultado en staging: 80,129 filas; 18,497 con tipo de venta, 11,013 pagados.
BEGIN;
UPDATE stock_picking sp
SET x_studio_tipo_de_venta = so.sale_type,
    x_studio_completamente_pagado = COALESCE(so.completely_paid, false)
FROM sale_order so
WHERE sp.sale_id = so.id;
COMMIT;
