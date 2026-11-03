-- Recuperación de configuración y datos menores 16 -> 19:
--  - Tipos de ausencia que son incapacidad (almx_incapacidad_dias_naturales): 60, 61, 62
--  - Fechas de tickets de Structural Elevation (almx_structural_elev): 30
--  - Nombre de archivo de Formatos Acabados en tareas (almx_guiasm): 10
-- Origen: producción 16 al cierre del 30-oct-2026.
BEGIN;
UPDATE hr_leave_type SET is_incapacidad = (id IN (60,61,62));
UPDATE helpdesk_ticket SET start_date='2026-07-31 18:42:23', effective_date=NULL, end_date=NULL WHERE id=9768;
UPDATE helpdesk_ticket SET start_date='2026-07-24 17:02:24', effective_date='2026-07-24 21:35:11', end_date='2026-07-24 21:35:11' WHERE id=9798;
UPDATE helpdesk_ticket SET start_date='2026-07-06 17:00:05', effective_date='2026-07-06 17:00:05', end_date='2026-07-06 20:59:44' WHERE id=9809;
UPDATE helpdesk_ticket SET start_date='2026-07-27 21:35:27', effective_date='2026-07-28 21:35:27', end_date='2026-07-28 21:40:55' WHERE id=9865;
UPDATE helpdesk_ticket SET start_date='2026-07-28 21:47:20', effective_date='2026-07-28 21:47:20', end_date='2026-07-28 21:47:20' WHERE id=9876;
UPDATE helpdesk_ticket SET start_date='2026-08-05 19:38:51', effective_date='2026-08-07 19:38:51', end_date='2026-08-11 19:58:04' WHERE id=9904;
UPDATE helpdesk_ticket SET start_date='2026-08-03 17:31:57', effective_date='2026-08-05 16:52:35', end_date='2026-08-05 17:32:23' WHERE id=9905;
UPDATE helpdesk_ticket SET start_date='2026-08-12 19:53:03', effective_date='2026-08-18 19:53:03', end_date='2026-08-18 19:53:03' WHERE id=9906;
UPDATE helpdesk_ticket SET start_date='2026-08-10 19:29:51', effective_date='2026-08-10 19:29:51', end_date='2026-08-11 19:34:27' WHERE id=9913;
UPDATE helpdesk_ticket SET start_date='2026-08-13 17:23:58', effective_date='2026-08-14 17:23:58', end_date='2026-08-14 17:30:54' WHERE id=9919;
UPDATE helpdesk_ticket SET start_date='2026-08-13 19:51:06', effective_date='2026-08-17 19:51:06', end_date='2026-08-18 19:51:06' WHERE id=9923;
UPDATE helpdesk_ticket SET start_date='2026-08-17 17:47:40', effective_date='2026-08-17 17:47:40', end_date='2026-08-18 19:48:10' WHERE id=9927;
UPDATE helpdesk_ticket SET start_date='2026-08-27 15:13:37', effective_date='2026-08-27 20:42:13', end_date='2026-08-27 20:42:22' WHERE id=9932;
UPDATE helpdesk_ticket SET start_date='2026-09-04 00:56:56', effective_date='2026-09-03 23:22:58', end_date='2026-09-04 23:22:49' WHERE id=9935;
UPDATE helpdesk_ticket SET start_date='2026-09-04 00:56:29', effective_date=NULL, end_date=NULL WHERE id=9956;
UPDATE helpdesk_ticket SET start_date='2026-09-16 19:00:05', effective_date='2026-09-17 19:00:05', end_date='2026-09-21 19:00:05' WHERE id=9957;
UPDATE helpdesk_ticket SET start_date='2026-08-31 23:36:34', effective_date='2026-08-31 23:36:30', end_date='2026-08-31 23:36:30' WHERE id=9979;
UPDATE helpdesk_ticket SET start_date='2026-09-08 19:34:35', effective_date='2026-09-09 17:47:50', end_date=NULL WHERE id=10003;
UPDATE helpdesk_ticket SET start_date='2026-09-21 14:59:42', effective_date='2026-09-21 14:59:42', end_date='2026-09-22 14:59:42' WHERE id=10029;
UPDATE helpdesk_ticket SET start_date='2026-10-01 17:22:17', effective_date='2026-10-02 23:38:27', end_date='2026-10-02 23:38:27' WHERE id=10058;
UPDATE helpdesk_ticket SET start_date='2026-10-06 15:03:00', effective_date='2026-10-07 15:03:00', end_date='2026-10-07 15:03:00' WHERE id=10066;
UPDATE helpdesk_ticket SET start_date='2026-10-12 22:50:28', effective_date=NULL, end_date=NULL WHERE id=10076;
UPDATE helpdesk_ticket SET start_date='2026-10-13 22:10:49', effective_date=NULL, end_date=NULL WHERE id=10079;
UPDATE helpdesk_ticket SET start_date='2026-10-27 21:58:08', effective_date='2026-10-30 15:56:03', end_date='2026-10-30 15:56:03' WHERE id=10081;
UPDATE helpdesk_ticket SET start_date='2026-10-20 23:42:10', effective_date='2026-10-28 20:53:11', end_date='2026-10-28 20:53:11' WHERE id=10085;
UPDATE helpdesk_ticket SET start_date='2026-10-16 20:28:30', effective_date='2026-10-19 20:26:23', end_date='2026-10-19 20:29:02' WHERE id=10088;
UPDATE helpdesk_ticket SET start_date='2026-10-19 16:45:14', effective_date='2026-10-20 19:05:19', end_date='2026-10-20 19:00:55' WHERE id=10091;
UPDATE helpdesk_ticket SET start_date='2026-10-22 16:53:48', effective_date='2026-10-23 20:22:21', end_date='2026-10-23 20:22:21' WHERE id=10101;
UPDATE helpdesk_ticket SET start_date='2026-10-26 17:18:52', effective_date='2026-10-27 15:55:39', end_date='2026-10-27 15:53:27' WHERE id=10105;
UPDATE helpdesk_ticket SET start_date='2026-10-29 15:45:21', effective_date='2026-10-30 15:45:21', end_date='2026-10-30 15:45:21' WHERE id=10106;
UPDATE project_task SET format_finally_filename='CAÑON DE SAN MARCOS GMD  (20-10-26).pdf' WHERE id=14331;
UPDATE project_task SET format_finally_filename='FORMATO ACABADOS DE EQUIPOS JORGE MELGAREJO-ZONA DIAMANTE (2).pdf' WHERE id=14590;
UPDATE project_task SET format_finally_filename='ACABADOS PROYECTO MUSICO-VICTOR BOLAÑOS.pdf' WHERE id=14664;
UPDATE project_task SET format_finally_filename='Arq. Ferera (Hamdi)-3. PLANO DE FRENTES.pdf' WHERE id=14736;
UPDATE project_task SET format_finally_filename='Equipos duplex 16 niveles (14-08-026).pdf' WHERE id=14737;
UPDATE project_task SET format_finally_filename='ACABADOS LA CORONA-SO64633.pdf' WHERE id=14763;
UPDATE project_task SET format_finally_filename='ACABADOS AGUILA CHAMARTIN-VALQUIRICO SO57730.pdf' WHERE id=14779;
UPDATE project_task SET format_finally_filename='Formato Acabados cabina,piso,plafon, etc..  Homelift Highland 10 Bosque Real.pdf' WHERE id=14788;
UPDATE project_task SET format_finally_filename='ELEVADOR CORDOBA VER 19 OCT -2026 (3).pdf' WHERE id=14824;
UPDATE project_task SET format_finally_filename='GMP ARMANDO HERRERA 22-10-26.pdf' WHERE id=14825;
COMMIT;
