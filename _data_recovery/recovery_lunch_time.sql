-- Recuperación de lunch_start / lunch_end (hr.attendance) de Odoo 16 a 19.
--
-- Lee lunch16.csv, generado en producción 16 con:
--   \copy (SELECT id, employee_id, check_in, check_out, lunch_start, lunch_end, worked_hours FROM hr_attendance WHERE lunch_start IS NOT NULL OR lunch_end IS NOT NULL ORDER BY id) TO 'lunch16.csv' CSV HEADER
--
-- Uso, desde la carpeta donde esté lunch16.csv:
--   Prueba:  psql -v aplicar=0 -f recovery_lunch_time.sql
--   Aplicar: psql -v aplicar=1 -f recovery_lunch_time.sql
--
-- Solo copia la comida a registros cerrados, del mismo empleado y hora de entrada, sin
-- comida capturada en 19 y que cumplan las validaciones de almx_lunch_time. Se usa SQL
-- para no recalcular worked_hours ni horas extra del histórico. Las horas (UTC) se
-- copian tal cual. Se puede volver a correr sin duplicar.
--
-- Para revertir solo lo aplicado:
--   UPDATE hr_attendance a SET lunch_start = NULL, lunch_end = NULL FROM almx_lunch_16_aplicado l
--    WHERE a.id = l.id AND a.lunch_start IS NOT DISTINCT FROM l.lunch_start AND a.lunch_end IS NOT DISTINCT FROM l.lunch_end;
\set ON_ERROR_STOP on
BEGIN;

CREATE TEMP TABLE t16 (
    id integer PRIMARY KEY,
    employee_id integer,
    check_in timestamp,
    check_out timestamp,
    lunch_start timestamp,
    lunch_end timestamp,
    worked_hours double precision
) ON COMMIT DROP;
\copy t16 FROM 'lunch16.csv' CSV HEADER

CREATE TABLE IF NOT EXISTS almx_lunch_16_aplicado (
    id integer PRIMARY KEY,
    lunch_start timestamp,
    lunch_end timestamp,
    aplicado_el timestamp NOT NULL DEFAULT (now() AT TIME ZONE 'UTC')
);

CREATE TEMP TABLE clasif ON COMMIT DROP AS
SELECT t.id,
       t.lunch_start,
       t.lunch_end,
       CASE
           WHEN a.id IS NULL THEN '1 no existe en 19'
           WHEN a.employee_id IS DISTINCT FROM t.employee_id OR a.check_in IS DISTINCT FROM t.check_in THEN '2 otro empleado o entrada'
           WHEN a.lunch_start IS NOT NULL OR a.lunch_end IS NOT NULL THEN '3 ya tiene comida en 19'
           WHEN a.check_out IS NULL THEN '4 sigue abierto en 19'
           WHEN t.lunch_start IS NULL THEN '5 regreso sin inicio'
           WHEN t.lunch_start < a.check_in THEN '6 inicio antes de entrada'
           WHEN t.lunch_end < t.lunch_start THEN '7 regreso antes de inicio'
           WHEN t.lunch_start > a.check_out OR t.lunch_end > a.check_out THEN '8 comida despues de salida'
           ELSE '9 aplicable'
       END AS estado,
       abs(COALESCE(a.worked_hours, 0) - COALESCE(t.worked_hours, 0)) > 0.02 AS horas_distintas
  FROM t16 t
  LEFT JOIN hr_attendance a ON a.id = t.id;

\echo === Registros de 16 por estado
SELECT estado, count(*) AS registros, count(*) FILTER (WHERE horas_distintas) AS horas_trabajadas_distintas
  FROM clasif GROUP BY estado ORDER BY estado;

\echo === Periodo de los aplicables
SELECT min(a.check_in) AS desde, max(a.check_in) AS hasta, count(DISTINCT a.employee_id) AS empleados
  FROM clasif c JOIN hr_attendance a ON a.id = c.id WHERE c.estado = '9 aplicable';

WITH upd AS (
    UPDATE hr_attendance a
       SET lunch_start = c.lunch_start, lunch_end = c.lunch_end
      FROM clasif c
     WHERE a.id = c.id AND c.estado = '9 aplicable'
    RETURNING a.id, a.lunch_start, a.lunch_end
), ins AS (
    INSERT INTO almx_lunch_16_aplicado (id, lunch_start, lunch_end)
    SELECT id, lunch_start, lunch_end FROM upd
    ON CONFLICT (id) DO UPDATE SET lunch_start = EXCLUDED.lunch_start, lunch_end = EXCLUDED.lunch_end
    RETURNING 1
)
SELECT count(*) AS actualizados FROM ins;

\if :aplicar
    COMMIT;
    \echo === APLICADO
\else
    ROLLBACK;
    \echo === PRUEBA: no se guardo nada
\endif
