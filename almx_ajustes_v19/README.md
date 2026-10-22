# almx_ajustes_v19

Recupera en Odoo 19 lo que se perdió en la migración desde 16, según la
validación por áreas del 22 oct 2026.

| Área | Qué hace |
|---|---|
| Aprobaciones | Campo **Responsable** (solicitud y categoría) con regla de acceso; estado **Hecho** con botón *Marcar como hecho*, filtro y columna; **grupos de lectura** por categoría. Reemplaza al módulo `doppler` (Vauxoo). |
| Tiempo personal | Doble aprobación siempre en **dos pasos** (en 19 RH validaba en un clic); el jefe da el primero y RH puede darlo de respaldo (queda nota en el chatter); **nadie aprueba su propia ausencia**; tipos **"Solo RH"**: los empleados solo ven Trabajo fuera de oficina, Falta justificada con goce (70), Falta justificada sin goce y Vacaciones. |
| Soporte | Regla nativa regresada al criterio de 16: cada usuario ve **solo sus tickets**. Grupo **"Soporte: ver todas las mesas"** para IT, Calidad y Dirección. Grupo Administrador solo para IT. |
| Almuerzos | Lista de pedidos editable en línea con **precio editable** (solo Responsable de almuerzos). |
| Reclutamiento | Método `format_date_to_tz` para la plantilla **Job Offer (AADM-MX-RH-FO-009)**; archiva la copia vieja del formulario de postulación; elimina el script huérfano de reCAPTCHA (OCA). |
| Empleados | **Fecha de ingreso, salida y motivo** juntos en la pestaña Trabajo; pestaña **Datos SAT / IMSS** de solo consulta. |

## Instalación (staging de Odoo.sh)

1. Subir `almx_ajustes_v19/` a `italam-max/doppler_19` y al repo de Odoo.sh
   (`/home/odoo/src/user`, rama staging).
2. Instalar el módulo. El `post_init_hook` asigna grupos, limpia Soporte /
   Administrador, marca los tipos "Solo RH" y archiva la vista vieja del sitio.
3. Generar y aplicar la recuperación de datos de 16 (ver `_data_recovery/`).

## Recuperación de datos (`_data_recovery/`)

`generar_sql_desde_16.py` lee de 16 por XML-RPC (API key) y genera:

* `01_aprobaciones.sql` – responsables, estado Hecho, grupos de lectura.
* `02_candidatos_notas.sql` – notas de candidatos (`description` → `applicant_notes`).
* `03_empleados_sat.sql` – datos SAT/IMSS. **Datos personales: no se versiona.**

Se aplican con `psql -v ON_ERROR_STOP=1 -f <archivo>` después de instalar el
módulo, y se vuelven a generar y correr en el corte del 1 nov.

## Pruebas sugeridas en staging

* Aprobaciones: aprobar una solicitud → *Marcar como hecho* → columna Hecho en kanban.
* Tiempo personal: con un usuario normal, el selector solo muestra 4 tipos;
  el jefe aprueba → queda en *Segunda aprobación* → RH valida; RH no puede
  validar su propia ausencia.
* Soporte: Zulit (o cualquier usuario sin el grupo) solo ve sus tickets.
* Almuerzos: el Responsable edita el precio en la lista.
* Reclutamiento: postular desde `/jobs` y mover un candidato a *Job Offer*.
* Empleados: pestañas Trabajo y Datos SAT / IMSS.
