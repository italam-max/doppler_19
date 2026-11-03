# -*- coding: utf-8 -*-
"""
_data_recovery/reasignar_diego_saul_19.py
=========================================
Pasa a Saúl Mata (saul.m) lo vigente de Diego (diego.u, inactivo; Saúl lo reemplazó).
Solo configuración y trabajo abierto: el historial (facturas, ausencias pasadas,
revisiones de calidad hechas, bitácoras) se queda con Diego.

  1. Responsable de tareas de actualización de producto (Verificación de SKU)
  2. Aprobador en categorías de Aprobaciones y en solicitudes pendientes
  3. Aprobador de ausencias y gastos de sus empleados
  4. Acciones automatizadas que le asignan actividades
  5. Responsable del proyecto y tareas abiertas
  6. Responsable de traslados abiertos
  7. Actividades abiertas (en traslados, solo los que siguen abiertos)
  8. Grupos operativos de Diego que Saúl no tenía
     (no: Ajustes, Administrador de Soporte, Documentos, Eventos, preferencia de notificación)
  9. Grupo Crear OUT manual (almx_stock_extends)

No se pasan: equipos asignados (laptop, mouse, cargador) ni actividades de traslados cerrados.
Idempotente. Uso:
  DRY_RUN=1 odoo-bin shell --no-http < _data_recovery/reasignar_diego_saul_19.py
  odoo-bin shell --no-http < _data_recovery/reasignar_diego_saul_19.py
"""
import os

DRY = os.environ.get('DRY_RUN') == '1'
env = env(context=dict(env.context, active_test=False, mail_activity_quick_update=True, mail_notify_noemail=True))
U = env['res.users']
diego = U.search([('login', '=', 'diego.u@alam.mx')], limit=1)
saul = U.search([('login', '=', 'saul.m@alam.mx')], limit=1)
assert diego and saul, 'No se encontró a Diego o a Saúl'
out, warn = [], []


def put(label, recs, vals):
    out.append('%-58s %d' % (label, len(recs)))
    if recs and not DRY:
        recs.write(vals)


put('1 Tareas de actualización de producto', env['almx.product.update.task'].search([('user_id', '=', diego.id)]),
    {'user_id': saul.id})

cat = env['approval.category.approver'].search([('user_id', '=', diego.id)])
dup = cat.filtered(lambda a: saul in a.category_id.approver_ids.user_id)
if dup:
    warn.append('Saúl ya era aprobador en: %s (se deja a Diego ahí)' % ', '.join(dup.category_id.mapped('name')))
put('2a Aprobador en categorías de Aprobaciones', cat - dup, {'user_id': saul.id})
put('2b Aprobador en solicitudes pendientes', env['approval.approver'].search([
    ('user_id', '=', diego.id), ('request_id.request_status', 'in', ('new', 'pending'))]), {'user_id': saul.id})

Emp = env['hr.employee']
put('3a Aprobador de ausencias de empleados', Emp.search([('leave_manager_id', '=', diego.id)]), {'leave_manager_id': saul.id})
put('3b Aprobador de gastos de empleados', Emp.search([('expense_manager_id', '=', diego.id)]), {'expense_manager_id': saul.id})

# El ORM no las encuentra por búsqueda (usuario inactivo); se ubican por SQL.
env.cr.execute('SELECT id FROM ir_act_server WHERE activity_user_id = %s', [diego.id])
acts = env['ir.actions.server'].browse([r[0] for r in env.cr.fetchall()])
out.append('%-58s %d' % ('4 Acciones automatizadas que asignan actividad', len(acts)))
if not DRY:
    for a in acts:
        a.write({'activity_user_id': saul.id, 'name': (a.name or '').replace('Diego', 'Saúl')})

put('5a Responsable de proyecto', env['project.project'].search([('user_id', '=', diego.id)]), {'user_id': saul.id})
put('5b Tareas abiertas asignadas', env['project.task'].search([
    ('user_ids', 'in', diego.ids), ('state', 'not in', ('1_done', '1_canceled'))]),
    {'user_ids': [(3, diego.id), (4, saul.id)]})

put('6 Traslados abiertos (responsable)', env['stock.picking'].search([
    ('user_id', '=', diego.id), ('state', 'not in', ('done', 'cancel'))]), {'user_id': saul.id})

open_pick = set(env['stock.picking'].search([('state', 'not in', ('done', 'cancel'))]).ids)
act = env['mail.activity'].search([('user_id', '=', diego.id)]).filtered(
    lambda a: a.res_model != 'stock.picking' or a.res_id in open_pick)
put('7 Actividades abiertas', act, {'user_id': saul.id})

GROUPS = ['mrp.group_mrp_user', '__export__.res_groups_96_3c582ed2', '__export__.res_groups_149_e068e368',
          '__export__.res_groups_187_258defe3', 'lunch.group_lunch_user',
          'almx_stock_extends.group_almx_manual_out_creator']
n = 0
for x in GROUPS:
    grp = env.ref(x, raise_if_not_found=False)
    if not grp:
        warn.append('grupo no encontrado: %s' % x)
        continue
    if saul not in grp.user_ids:
        n += 1
        if not DRY:
            grp.write({'user_ids': [(4, saul.id)]})
out.append('%-58s %d' % ('8-9 Grupos agregados a Saúl', n))

if DRY:
    env.cr.rollback()
else:
    env.cr.commit()
print('[%s] Diego (%s) -> Saúl (%s)' % ('DRY_RUN' if DRY else 'APLICADO', diego.login, saul.login))
print('\n'.join(out))
print('\n'.join('AVISO: ' + w for w in warn) or 'sin avisos')
