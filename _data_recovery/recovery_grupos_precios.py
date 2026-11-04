# -*- coding: utf-8 -*-
"""
_data_recovery/recovery_grupos_precios.py
=========================================
Recupera en 19 quién puede ver precios y costos de producto.

Los grupos doppler.group_can_see_prices, sale_order_invoice.group_sale_price_unit_user
y doppler.group_can_see_product_cost no llegaron a 19, pero las vistas de producto los
siguen usando, así que esos campos quedaron ocultos para todos.

Este script:
  1. Cambia esas referencias en las vistas por los grupos de almx_ajustes_v19.
  2. Asigna los usuarios que tenían en producción 16 (consulta del 4-nov-2026).
     Los usuarios inactivos en 19 no se asignan; solo se reportan.

Solo toca vistas activas. Las inactivas conservan la referencia vieja: 6 de ellas
ya están rotas (primarias sin vista padre) y no se pueden validar ni se usan.

Requiere almx_ajustes_v19 >= 19.0.1.0.1 ya actualizado. Idempotente: solo agrega.
Si una vista no valida, se cancela todo y no se guarda nada. La arquitectura
anterior de cada vista queda en arch_prev.

Uso:
  DRY_RUN=1 odoo-bin shell --no-http < _data_recovery/recovery_grupos_precios.py
  odoo-bin shell --no-http < _data_recovery/recovery_grupos_precios.py
"""
import os
import re

DRY = os.environ.get('DRY_RUN') == '1'
PRICES = 'almx_ajustes_v19.group_can_see_prices'
COST = 'almx_ajustes_v19.group_can_see_product_cost'
OLD_PRICES = 'doppler.group_can_see_prices'
OLD_UNIT = 'sale_order_invoice.group_sale_price_unit_user'
OLD_COST = 'doppler.group_can_see_product_cost'

REPLACEMENTS = [
    (re.compile(r'%s\s*,\s*%s' % (re.escape(OLD_PRICES), re.escape(OLD_UNIT))), PRICES),
    (re.compile(r'%s\s*,\s*%s' % (re.escape(OLD_UNIT), re.escape(OLD_PRICES))), PRICES),
    (re.compile(re.escape(OLD_PRICES)), PRICES),
    (re.compile(re.escape(OLD_UNIT)), PRICES),
    (re.compile(re.escape(OLD_COST)), COST),
]

PRICE_USERS = [
    'admin.cuentas@alam.mx', 'alexis.a@alam.mx', 'angelica.g@alam.mx', 'becario@alam.mx',
    'carlos.s@alam.mx', 'celia.a@alam.mx', 'david.e@alam.mx', 'eliana.z@alam.mx',
    'gerardo.b@alam.mx', 'hamdi@alam.mx', 'helmi@alam.mx', 'italam@alam.mx',
    'javier.s@alam.mx', 'joud@alam.mx', 'karina.m@alam.mx', 'kesia.d@alam.mx',
    'leonel.j@alam.mx', 'liliana@alamex.com.tr', 'martha.r@alam.mx', 'oscar.a@alam.mx',
    'silvia.f@alam.mx', 'sinue@alam.mx', 'sonia.g@alam.mx', 'valente.c@alam.mx',
]
COST_USERS = [
    'admin.cuentas@alam.mx', 'alexis.a@alam.mx', 'angelica.g@alam.mx', 'celia.a@alam.mx',
    'hamdi@alam.mx', 'helmi@alam.mx', 'italam@alam.mx', 'javier.s@alam.mx', 'joud@alam.mx',
    'karina.m@alam.mx', 'leonel.j@alam.mx', 'martha.r@alam.mx', 'silvia.f@alam.mx',
    'valente.c@alam.mx',
]

env = env(context=dict(env.context, lang='en_US'))  # noqa: F821 (odoo shell)

group_prices = env.ref(PRICES, raise_if_not_found=False)
group_cost = env.ref(COST, raise_if_not_found=False)
if not group_prices or not group_cost:
    raise RuntimeError('Faltan los grupos: primero actualiza almx_ajustes_v19 a 19.0.1.0.1')

# 1. Vistas
View = env['ir.ui.view']
views = View.search(['|', '|',
                     ('arch_db', 'ilike', OLD_PRICES),
                     ('arch_db', 'ilike', OLD_UNIT),
                     ('arch_db', 'ilike', OLD_COST)])
n_views = 0
for view in views:
    arch = view.arch_db
    for pattern, new in REPLACEMENTS:
        arch = pattern.sub(new, arch)
    if arch != view.arch_db:
        n_views += 1
        view.write({'arch_db': arch})  # valida la vista; si falla, se cancela todo

# 2. Usuarios
inactive = set()
missing = set()
n_links = 0
for group, logins in ((group_prices, PRICE_USERS), (group_cost, COST_USERS)):
    for login in logins:
        user = env['res.users'].with_context(active_test=False).search([('login', '=', login)], limit=1)
        if not user:
            missing.add(login)
        elif not user.active:
            inactive.add(login)
        elif user not in group.user_ids:
            n_links += 1
            group.write({'user_ids': [(4, user.id)]})

old_domain = ['|', '|',
              ('arch_db', 'ilike', OLD_PRICES),
              ('arch_db', 'ilike', OLD_UNIT),
              ('arch_db', 'ilike', OLD_COST)]
left = View.search_count(old_domain)
left_inactive = View.with_context(active_test=False).search_count([('active', '=', False)] + old_domain)
print('[%s] vistas activas actualizadas: %d | activas con referencia vieja: %d | inactivas sin tocar: %d'
      % ('DRY_RUN' if DRY else 'APLICADO', n_views, left, left_inactive))
print('usuarios agregados a grupos: %d' % n_links)
print('usuarios en "%s": %d | en "%s": %d'
      % (group_prices.name, len(group_prices.user_ids), group_cost.name, len(group_cost.user_ids)))
print('inactivos en 19 (no asignados): %s' % (', '.join(sorted(inactive)) or 'ninguno'))
print('no existen en 19: %s' % (', '.join(sorted(missing)) or 'ninguno'))

if DRY:
    env.cr.rollback()
else:
    env.cr.commit()
    env.registry.signal_changes()  # avisa a los demás procesos que cambiaron las vistas
