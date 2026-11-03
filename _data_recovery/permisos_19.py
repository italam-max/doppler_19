# -*- coding: utf-8 -*-
"""
_data_recovery/permisos_19.py
=============================
Restaura en 19 los permisos que en el staging validado se ajustaron a mano
(ensayo de corte 14-oct-2026, diff contra el staging validado por áreas):

  - 90 asignaciones usuario -> grupo (grupos de almx_* y algunos estándar)
  - 33 accesos (ir.model.access) faltantes
  - 78 reglas de registro custom que el upgrade dejó inactivas
  - 3 reglas de registro faltantes y 1 dominio a corregir
  - Secuencia de folios AJU (stock.adjustment.request) después del recovery SQL

Idempotente: se puede correr N veces. Correr DESPUÉS de instalar los almx_*
y de los SQL de _data_recovery.

Uso (shell de Odoo.sh, desde la carpeta del repo doppler_19):
  DRY_RUN=1 odoo-bin shell < _data_recovery/permisos_19.py   # prueba
  odoo-bin shell < _data_recovery/permisos_19.py             # aplica
Lee la especificación de _data_recovery/permisos_19.json (o PERM_SPEC=ruta).
"""
import json
import os
import time

t0 = time.time()
DRY = os.environ.get('DRY_RUN') == '1'
spec_path = os.environ.get('PERM_SPEC', '_data_recovery/permisos_19.json')
spec = json.load(open(spec_path, encoding='utf-8'))
env = env(context=dict(env.context, active_test=False))  # noqa: F821 (odoo shell)
log = {'ok': [], 'warn': []}


def group(ref):
    if ref.startswith('#'):  # grupo sin xmlid: se busca por nombre
        g = env['res.groups'].search([('name', '=', ref[1:])], limit=2)
        if len(g) != 1:
            log['warn'].append('grupo no resuelto: %s' % ref)
            return env['res.groups']
        return g
    g = env.ref(ref, raise_if_not_found=False)
    if not g:
        log['warn'].append('grupo no encontrado: %s' % ref)
        return env['res.groups']
    return g


def model_id(name):
    m = env['ir.model'].search([('model', '=', name)], limit=1)
    if not m:
        log['warn'].append('modelo no encontrado: %s' % name)
    return m


def perms(p):
    return dict(perm_read=p[0] == '1', perm_write=p[1] == '1',
                perm_create=p[2] == '1', perm_unlink=p[3] == '1')


# 1. Usuarios en grupos
n = 0
for ref, logins in spec['members'].items():
    g = group(ref)
    if not g:
        continue
    for lg in logins:
        login = lg if '@' in lg else lg + '@alam.mx'
        u = env['res.users'].search([('login', '=', login)], limit=1)
        if not u:
            log['warn'].append('usuario no encontrado: %s' % login)
            continue
        if u not in g.user_ids:
            n += 1
            if not DRY:
                g.write({'user_ids': [(4, u.id)]})
log['ok'].append('usuarios agregados a grupos: %d' % n)

# 2. Accesos
n = 0
for mname, gref, p in spec['access']:
    m = model_id(mname)
    g = group(gref) if gref else env['res.groups']
    if not m or (gref and not g):
        continue
    dom = [('model_id', '=', m.id), ('group_id', '=', g.id or False)]
    dom += [(k, '=', v) for k, v in perms(p).items()]
    if env['ir.model.access'].search_count(dom):
        continue
    n += 1
    if not DRY:
        vals = dict(perms(p), model_id=m.id, group_id=g.id or False,
                    name='almx_19 %s %s' % (mname, gref or 'all'))
        env['ir.model.access'].create(vals)
log['ok'].append('accesos creados: %d' % n)

# 3. Reglas: reactivar, crear, corregir dominio
Rule = env['ir.rule']
n = 0
for mname, names in spec['rules_on'].items():
    m = model_id(mname)
    for nm in names:
        r = Rule.search([('model_id', '=', m.id), ('name', '=', nm)])
        if not r:
            log['warn'].append('regla no encontrada: %s | %s' % (mname, nm))
            continue
        todo = r.filtered(lambda x: not x.active)
        n += len(todo)
        if todo and not DRY:
            todo.write({'active': True})
log['ok'].append('reglas reactivadas: %d' % n)

n = 0
for mname, nm, dom, grefs, p in spec['rules_new']:
    m = model_id(mname)
    if not m or Rule.search_count([('model_id', '=', m.id), ('name', '=', nm)]):
        continue
    gids = [g.id for g in map(group, grefs) if g]
    n += 1
    if not DRY:
        Rule.create(dict(perms(p), name=nm, model_id=m.id, domain_force=dom,
                         groups=[(6, 0, gids)]))
log['ok'].append('reglas creadas: %d' % n)

n = 0
for mname, nm, dom in spec['rules_dom']:
    m = model_id(mname)
    r = Rule.search([('model_id', '=', m.id), ('name', '=', nm)])
    todo = r.filtered(lambda x: x.domain_force != dom)
    n += len(todo)
    if todo and not DRY:
        todo.write({'domain_force': dom})
log['ok'].append('dominios corregidos: %d' % n)

# 4. Secuencia de folios AJU
if 'stock.adjustment.request' in env:
    reqs = env['stock.adjustment.request'].search([('name', '=like', 'AJU/%')])
    top = max([int(x.name.rsplit('/', 1)[-1]) for x in reqs if x.name.rsplit('/', 1)[-1].isdigit()] or [0])
    seq = env['ir.sequence'].search([('code', '=', 'stock.adjustment.request')], limit=1)
    if seq and top and seq.number_next_actual <= top:
        if not DRY:
            seq.number_next_actual = top + 1
        log['ok'].append('secuencia AJU -> %d' % (top + 1))
    elif not seq:
        log['warn'].append('secuencia stock.adjustment.request no encontrada')

if DRY:
    env.cr.rollback()
else:
    env.cr.commit()
print('\n'.join(['[%s] %.1fs' % ('DRY_RUN' if DRY else 'APLICADO', time.time() - t0)]
                + log['ok'] + ['AVISO: ' + w for w in log['warn']]))
