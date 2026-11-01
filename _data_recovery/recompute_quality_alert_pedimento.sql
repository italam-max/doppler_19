-- Recalculo de quality_alert.entry_number (related guardado a stock_picking.entry_number,
-- almx_quality_extends). Correr DESPUES de recovery_entry_number.sql: el SQL directo
-- no dispara el recalculo de los campos guardados que dependen de la columna.
-- Resultado en staging (1-nov-2026): 46 alertas resincronizadas.
BEGIN;
UPDATE quality_alert qa
SET entry_number = sp.entry_number
FROM stock_picking sp
WHERE sp.id = qa.picking_id
  AND qa.entry_number IS DISTINCT FROM sp.entry_number;
COMMIT;
