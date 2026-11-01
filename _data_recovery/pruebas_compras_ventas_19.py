# -*- coding: utf-8 -*-
"""
_data_recovery/pruebas_compras_ventas_19.py
===========================================
Pruebas de Compras / Ventas / Producto en 19 con usuarios reales (with_user).
Cada prueba corre en un savepoint y al final TODO se revierte: no deja datos.
Correr DESPUÉS de los _data_recovery y permisos_19.py.

Uso: odoo-bin shell --no-http < _data_recovery/pruebas_compras_ventas_19.py
"""
import base64

R = []


class Rollback(Exception):
    pass


def run(name, fn, expect):
    """expect: texto esperado en el error, callable(resultado) -> bool, o None (informativo)."""
    try:
        with env.cr.savepoint():
            raise Rollback(fn())
    except Rollback as r:
        res = r.args[0]
        st = 'INFO' if expect is None else ('OK' if callable(expect) and expect(res) else 'FALLA')
        R.append((st, name, 'sin error -> %s' % str(res)[:170]))
    except Exception as e:
        msg = ' '.join(str(e).split())
        st = 'OK' if isinstance(expect, str) and expect.lower() in msg.lower() else ('INFO' if expect is None else 'FALLA')
        R.append((st, name, '%s: %s' % (type(e).__name__, msg[:170])))
    finally:
        env.invalidate_all()


def skip(name, why):
    R.append(('S/C', name, why))


Users = env['res.users']


def user(*logins):
    for lg in logins:
        u = Users.search([('login', '=', lg + '@alam.mx')], limit=1)
        if u:
            return u
    return Users


vend = user('sinue')            # vendedor, sin permiso de precio ni de alta de productos
crea = user('leonel.j')         # grupo Permitir Crear Productos
precio = user('javier.s')       # grupo Editar precio de venta
hamdi = user('hamdi')
compras = (env.ref('purchase.group_purchase_user').user_ids.filtered(
    lambda u: u.active and not u.share and u.login.split('@')[0] not in ('italam', 'hamdi', 'admin'))[:1])

# --- Alta de productos ---
run('01 Crear producto (vendedor %s)' % vend.login, lambda: env['product.template'].with_user(vend).create(
    {'name': 'PRUEBA 19 NO USAR'}).id, 'No tienes permisos para crear nuevos productos')
run('02 Crear producto (%s, grupo alta)' % crea.login, lambda: env['product.template'].with_user(crea).create(
    {'name': 'PRUEBA 19 NO USAR'}).id, lambda r: bool(r))

# --- Precio de venta ---
tmpl = env['product.template'].search([('sale_ok', '=', True), ('list_price', '>', 0),
                                      ('product_variant_count', '=', 1)], order='id desc', limit=1)
run('03 Cambiar precio (vendedor)', lambda: tmpl.with_user(vend).write({'list_price': tmpl.list_price + 1}),
    'No tienes permiso para modificar el Precio de venta')


def precio_ok():
    n0 = env['mail.tracking.value'].search_count([('mail_message_id.model', '=', 'product.template'),
                                                  ('mail_message_id.res_id', '=', tmpl.id),
                                                  ('field_id.name', '=', 'list_price')])
    tmpl.with_user(precio).write({'list_price': tmpl.list_price + 1})
    env.flush_all()
    n1 = env['mail.tracking.value'].search_count([('mail_message_id.model', '=', 'product.template'),
                                                  ('mail_message_id.res_id', '=', tmpl.id),
                                                  ('field_id.name', '=', 'list_price')])
    return 'registrado en chatter' if n1 > n0 else 'SIN registro'


run('04 Cambiar precio (%s, grupo precio) queda en chatter' % precio.login, precio_ok,
    lambda r: r == 'registrado en chatter')

# --- Precio por variante ---
pv = env['product.product'].search([('variant_price', '>', 0)], limit=1)
if pv:
    run('05 Variante con precio propio: lst_price y lista = variant_price', lambda: (
        pv.variant_price, pv.lst_price, pv._price_compute('list_price')[pv.id]),
        lambda r: r[0] == r[1] == r[2])

    def var_indep():
        sib = pv.product_tmpl_id.product_variant_ids - pv
        before = (pv.product_tmpl_id.list_price, sib.mapped('lst_price'))
        pv.with_user(hamdi).write({'variant_price': pv.variant_price + 1})
        env.invalidate_all()
        after = (pv.product_tmpl_id.list_price, sib.mapped('lst_price'))
        return before == after

    run('06 Editar precio de variante no mueve plantilla ni hermanas', var_indep, lambda r: r is True)
    run('07 Editar precio de variante (vendedor)', lambda: pv.with_user(vend).write(
        {'variant_price': pv.variant_price + 1}), 'No tienes permiso para modificar el Precio de venta')
else:
    skip('05-07 Precio por variante', 'no hay variantes con precio propio')

# --- Compras de importación ---
nac = env['res.partner'].search([('supplier_rank', '>', 0), ('is_company', '=', True),
                                 ('almx_import_vendor', '=', False), ('country_id.code', '=', 'MX')], limit=1)
if compras:
    run('08 PO a proveedor de importación (%s)' % compras.login, lambda: env['purchase.order'].with_user(compras).create(
        {'partner_id': 17886}).almx_is_import, lambda r: r is True)
    run('09 PO a proveedor nacional (%s)' % nac.name, lambda: env['purchase.order'].with_user(compras).create(
        {'partner_id': nac.id}).almx_is_import, lambda r: r is False)
else:
    skip('08-09 PO importación', 'no hay usuario de Compras')

# --- Almacén de retirada (almx_gdl) ---
Quant = env['stock.quant']
Loc = env['stock.location']
alm2, gdl = Loc.browse(1519), Loc.browse(3600)
cust = env['sale.order'].search([('state', '=', 'sale')], order='id desc', limit=1).partner_id
q2 = Quant.search([('location_id', 'child_of', alm2.id), ('quantity', '>', 1), ('product_id.sale_ok', '=', True)], limit=300)
p_sin_gdl = q2.product_id.filtered(lambda p: p.is_storable and Quant._get_available_quantity(p, gdl) <= 0)[:1]
qg = Quant.search([('location_id', 'child_of', gdl.id), ('quantity', '>', 1), ('product_id.sale_ok', '=', True)], limit=300)
p_gdl = qg.product_id.filtered(lambda p: p.is_storable and Quant._get_available_quantity(p, gdl) > 0)[:1]


def so_line(product, loc):
    so = env['sale.order'].with_user(vend).create({'partner_id': cust.id, 'sale_type': 'spare', 'order_line': [
        (0, 0, {'product_id': product.id, 'product_uom_qty': 1, 'x_almacen_retirada_id': loc.id})]})
    line = so.order_line[:1]
    line._onchange_almacen_retirada_id()
    return 'ruta GDL=%s' % (line._get_route_gdl() in line.route_ids)


if p_sin_gdl:
    run('10 Retirar de GDL sin existencia (%s)' % p_sin_gdl.default_code, lambda: so_line(p_sin_gdl, gdl),
        'no hay existencia')
else:
    skip('10 Retirada sin existencia', 'sin producto adecuado')
if p_gdl:
    run('11 Retirar de GDL con existencia agrega ruta GDL (%s)' % p_gdl.default_code, lambda: so_line(p_gdl, gdl),
        lambda r: r == 'ruta GDL=True')
else:
    skip('11 Retirada GDL', 'sin producto con existencia en GDL')

# --- Solicitud de actualización de producto ---
tasks = env['almx.product.update.task'].search([])
R.append(('INFO', '12a Responsables de actualización', '; '.join(
    '%s=%s%s' % (t.name, t.user_id.login.split('@')[0] if t.user_id else '-', '' if t.user_id.active else ' (INACTIVO)')
    for t in tasks)))
if compras:
    run('12b Solicitar actualización (%s)' % compras.login, lambda: tmpl.with_user(compras)
        .action_solicitar_actualizacion_producto()['params']['message'], lambda r: 'Se crearon' in r)

# --- Contactos ---


def csf():
    p = cust.commercial_partner_id
    n0 = len(p.message_ids)
    p.with_user(vend).write({'csf_document': base64.b64encode(b'%PDF-1.4 prueba'), 'csf_document_filename': 'csf_prueba.pdf'})
    env.invalidate_all()
    return len(p.message_ids) - n0


run('13 Adjuntar CSF deja registro en chatter (vendedor)', csf, lambda r: r > 0)


def desync():
    env.cr.execute("""select count(*) from quality_alert qa join stock_picking sp on sp.id = qa.picking_id
                      where qa.entry_number is distinct from sp.entry_number""")
    return env.cr.fetchone()[0]


run('14 Pedimento en alertas de calidad = recepción (diferencias)', desync, lambda r: r == 0)

env.cr.rollback()
print('Usuarios: vendedor=%s | alta=%s | precio=%s | compras=%s' % (vend.login, crea.login, precio.login, compras.login))
for s, n, d in R:
    print('%-5s %-62s %s' % (s, n, d))
print('Resumen: %d OK, %d FALLA, %d INFO, %d S/C  -- todo revertido (rollback)' % tuple(
    sum(1 for r in R if r[0] == k) for k in ('OK', 'FALLA', 'INFO', 'S/C')))
