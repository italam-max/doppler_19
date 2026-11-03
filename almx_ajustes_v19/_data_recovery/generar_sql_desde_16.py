#!/usr/bin/env python3
"""Genera los SQL de recuperación de datos 16 → 19 para almx_ajustes_v19.

Lee de Odoo 16 (producción) por XML-RPC y escribe un .sql por bloque en esta
misma carpeta. Los ids de registros coinciden entre 16 y 19 (misma base), así
que todo se actualiza por id. Cada sentencia valida que el registro exista en
19 antes de escribir.

Uso (desde cualquier equipo con acceso a alam.mx):

    export ODOO16_URL=https://www.alam.mx
    export ODOO16_DB=odoo13_backup_2024_12_14_09_55
    export ODOO16_USER=italam@alam.mx
    export ODOO16_KEY=<API key de 16>
    python3 generar_sql_desde_16.py

Después, en la shell de Odoo.sh (staging o producción), con el módulo ya
instalado:

    psql -v ON_ERROR_STOP=1 -f 01_aprobaciones.sql
    psql -v ON_ERROR_STOP=1 -f 02_candidatos_notas.sql
    psql -v ON_ERROR_STOP=1 -f 03_empleados_sat.sql
    psql -v ON_ERROR_STOP=1 -f 04_tareas_guias.sql

Los SQL con datos personales (03) NO se suben al repo: van en .gitignore.
"""
import os
import sys
import xmlrpc.client
from collections import defaultdict

URL = os.environ.get('ODOO16_URL', 'https://www.alam.mx')
DB = os.environ.get('ODOO16_DB', 'odoo13_backup_2024_12_14_09_55')
USER = os.environ.get('ODOO16_USER')
KEY = os.environ.get('ODOO16_KEY')
OUT = os.path.dirname(os.path.abspath(__file__))
BATCH = 2000

if not USER or not KEY:
    sys.exit('Define ODOO16_USER y ODOO16_KEY (API key) en el entorno.')

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
UID = common.authenticate(DB, USER, KEY, {})
if not UID:
    sys.exit('No se pudo autenticar en Odoo 16.')
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object', allow_none=True)
CTX = {'active_test': False}


def search_read(model, domain, fields):
    rows, offset = [], 0
    while True:
        batch = models.execute_kw(DB, UID, KEY, model, 'search_read', [domain],
                                  {'fields': fields, 'offset': offset, 'limit': BATCH,
                                   'order': 'id', 'context': CTX})
        rows += batch
        if len(batch) < BATCH:
            return rows
        offset += BATCH


def lit(value):
    """Literal SQL seguro (texto con comillas escapadas, NULL para vacío)."""
    if value in (False, None, ''):
        return 'NULL'
    if isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def m2o(value):
    return value[0] if value else None


def chunks(seq, size=1000):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def write(name, lines):
    path = os.path.join(OUT, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('BEGIN;\n')
        f.write('\n'.join(lines))
        f.write('\nCOMMIT;\n')
    print(f'  {name}: {len(lines)} sentencias')


# ---------------------------------------------------------------------------
# 01 Aprobaciones: responsable, estado Hecho, grupos de lectura y responsable
#    de categoría (módulo doppler de 16)
# ---------------------------------------------------------------------------
def aprobaciones():
    lines = ['-- Aprobaciones (doppler 16 → almx_ajustes_v19)']
    reqs = search_read('approval.request', [], ['responsible_id', 'request_status'])
    by_user = defaultdict(list)
    done = []
    for r in reqs:
        if r['responsible_id']:
            by_user[r['responsible_id'][0]].append(r['id'])
        if r['request_status'] == 'done':
            done.append(r['id'])
    for user_id, ids in by_user.items():
        for part in chunks(ids):
            lines.append(
                f"UPDATE approval_request SET responsible_id = {user_id} "
                f"WHERE id IN ({','.join(map(str, part))}) "
                f"AND EXISTS (SELECT 1 FROM res_users WHERE id = {user_id});")
    for part in chunks(done):
        lines.append(
            "UPDATE approval_request SET request_status = 'done' "
            f"WHERE id IN ({','.join(map(str, part))});")

    cats = search_read('approval.category', [], ['responsible_id', 'read_group_ids'])
    for c in cats:
        if c['responsible_id']:
            uid = c['responsible_id'][0]
            lines.append(
                f"UPDATE approval_category SET responsible_id = {uid} WHERE id = {c['id']} "
                f"AND EXISTS (SELECT 1 FROM res_users WHERE id = {uid});")
        for gid in c['read_group_ids']:
            lines.append(
                "INSERT INTO approval_category_read_groups (approval_category_id, res_group_id) "
                f"SELECT {c['id']}, {gid} WHERE EXISTS (SELECT 1 FROM approval_category WHERE id = {c['id']}) "
                f"AND EXISTS (SELECT 1 FROM res_groups WHERE id = {gid}) ON CONFLICT DO NOTHING;")
    print(f"Aprobaciones: {sum(map(len, by_user.values()))} responsables, {len(done)} en Hecho, "
          f"{len(cats)} categorías")
    write('01_aprobaciones.sql', lines)


# ---------------------------------------------------------------------------
# 02 Reclutamiento: descripción del candidato (16) → applicant_notes (19)
#    Solo se escribe donde 19 no tiene notas, para no pisar lo capturado.
# ---------------------------------------------------------------------------
def candidatos():
    lines = ['-- Notas de candidatos: hr.applicant.description (16) → applicant_notes (19)']
    apps = search_read('hr.applicant', [('description', '!=', False)], ['description'])
    for a in apps:
        lines.append(
            f"UPDATE hr_applicant SET applicant_notes = {lit(a['description'])} "
            f"WHERE id = {a['id']} AND (applicant_notes IS NULL OR applicant_notes = '' "
            f"OR applicant_notes = '<p><br></p>');")
    print(f'Candidatos: {len(apps)} notas')
    write('02_candidatos_notas.sql', lines)


# ---------------------------------------------------------------------------
# 03 Empleados: datos SAT / IMSS de nomina_cfdi_ee (16) → almx_* (19)
#    CONTIENE DATOS PERSONALES: no subir al repo.
# ---------------------------------------------------------------------------
CFDI_MAP = {
    'no_empleado': 'almx_no_empleado',
    'rfc': 'almx_rfc',
    'curp': 'almx_curp',
    'segurosocial': 'almx_nss',
    'empleado_nombre': 'almx_nombre',
    'empleado_paterno': 'almx_apellido_paterno',
    'empleado_materno': 'almx_apellido_materno',
    'registro_patronal_id': 'almx_registro_patronal',
    'regimen': 'almx_regimen',
    'contrato': 'almx_contrato',
    'jornada': 'almx_jornada',
    'sindicalizado': 'almx_sindicalizado',
    'estado': 'almx_estado_labora_id',
    'domicilio_receptor': 'almx_cp_fiscal',
}


def empleados():
    lines = ['-- Datos SAT / IMSS (nomina_cfdi_ee 16 → almx_ajustes_v19). DATOS PERSONALES.']
    emps = search_read('hr.employee', ['|', ('rfc', '!=', False), ('curp', '!=', False)],
                       list(CFDI_MAP))
    for e in emps:
        sets = []
        for src, dst in CFDI_MAP.items():
            val = e[src]
            if src == 'registro_patronal_id':
                val = val[1] if val else None
            elif src == 'estado':
                val = m2o(val)
            elif src == 'sindicalizado':
                val = bool(val)
            sets.append(f'{dst} = {lit(val)}')
        lines.append(f"UPDATE hr_employee SET {', '.join(sets)} WHERE id = {e['id']};")
    print(f'Empleados: {len(emps)} con datos SAT/IMSS')
    write('03_empleados_sat.sql', lines)


# ---------------------------------------------------------------------------
# 04 Proyectos: end_guides de almx_project (16), deprecado en 19
# ---------------------------------------------------------------------------
def tareas():
    lines = ['-- Guías terminadas (referencia): project.task.end_guides (almx_project 16)']
    tasks = search_read('project.task', [('end_guides', '!=', False)], ['end_guides'])
    for t in tasks:
        lines.append(f"UPDATE project_task SET end_guides = {lit(t['end_guides'])} WHERE id = {t['id']};")
    print(f'Tareas: {len(tasks)} con guías terminadas')
    write('04_tareas_guias.sql', lines)


if __name__ == '__main__':
    print(f'Leyendo de {URL} ({DB})…')
    aprobaciones()
    candidatos()
    empleados()
    tareas()
    print('Listo.')
