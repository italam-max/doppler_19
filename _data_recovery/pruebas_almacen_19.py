# -*- coding: utf-8 -*-
"""
_data_recovery/pruebas_almacen_19.py
====================================
Pruebas de los candados de almacén en 19 con usuarios reales (with_user).
Cada prueba corre en un savepoint y al final TODO se revierte: no deja datos.
Correr DESPUÉS de config_almacen_19.py y permisos_19.py.

Uso: odoo-bin shell --no-http < _data_recovery/pruebas_almacen_19.py
"""
import re

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
        R.append((st, name, 'sin error -> %s' % str(res)[:160]))
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


DIR = env.ref('almx_stock_movement_guard.group_direccion').user_ids
alm = user('entregas', 'leonel.j')
hamdi = user('hamdi')
wh = env['stock.warehouse'].search([('code', '=', 'WHTl')], limit=1)


def ptype(code, seq):
    return env['stock.picking.type'].search([('warehouse_id.code', '=', code), ('sequence_code', '=', seq)], limit=1)


OUT, INT, IN_, RET = ptype('WHTl', 'NWH/OUT/'), ptype('WHTl', 'NWH/INT/'), ptype('WHTl', 'NWH/IN/'), ptype('WHTl', 'RET')
cust = env.ref('stock.stock_location_customers')
supp = env.ref('stock.stock_location_suppliers')
merma = env['stock.location'].browse(376)
q = env['stock.quant'].search([('location_id', 'child_of', wh.lot_stock_id.id), ('location_id.usage', '=', 'internal'),
                               ('quantity', '>=', 2), ('reserved_quantity', '=', 0),
                               ('product_id.tracking', '=', 'none')], limit=1)
prod, src = q.product_id, q.location_id


def mk(pt, s, d):
    p = env['stock.picking'].create({
        'picking_type_id': pt.id, 'location_id': s.id, 'location_dest_id': d.id,
        'move_ids': [(0, 0, {'product_id': prod.id, 'product_uom_qty': 1, 'product_uom': prod.uom_id.id,
                             'location_id': s.id, 'location_dest_id': d.id})]})
    p.action_confirm()
    p.action_assign()
    return p


def val(p, u):
    res = p.with_user(u).button_validate()
    return p.state if res is True else res


# --- Candados de movimiento ---
run('01 OUT sin SO (almacén)', lambda: val(mk(OUT, src, cust), alm), 'no tiene Pedido de venta')
run('02 INT a Merma (almacén)', lambda: val(mk(INT, src, merma), alm), 'solo lo puede validar Dirección')
run('03 INT a Merma (Dirección)', lambda: val(mk(INT, src, merma), hamdi), lambda r: r == 'done')
run('04 IN manual sin PO (almacén)', lambda: val(mk(IN_, supp, IN_.default_location_dest_id), alm), 'recepción sin Orden de compra')
run('05 RET manual (almacén)', lambda: val(mk(RET, cust, RET.default_location_dest_id), alm), 'recepción sin Orden de compra')
run('06 Desechar material (almacén)', lambda: env['stock.scrap'].create({
    'product_id': prod.id, 'scrap_qty': 1, 'location_id': src.id, 'product_uom_id': prod.uom_id.id,
}).with_user(alm).do_scrap(), 'Solo Dirección puede desechar')


def adj():
    qq = q.with_user(alm)
    qq.inventory_quantity = q.quantity + 1
    return qq.action_apply_inventory()


run('07 Ajuste de inventario directo (almacén)', adj,
    lambda r: isinstance(r, dict) and r.get('res_model') == 'stock.adjustment.request.wizard')

# --- OUT existentes ligadas a SO ---
outs = env['stock.picking'].search([('picking_type_id', '=', OUT.id), ('state', '=', 'assigned'),
                                    ('sale_id', '!=', False)], order='id desc', limit=200)
o1 = outs[:1]
if o1:
    run('08 OUT congelado: agregar línea (almacén)', lambda: o1.with_user(alm).write({'move_ids': [(0, 0, {
        'product_id': prod.id, 'product_uom_qty': 1, 'product_uom': prod.uom_id.id,
        'location_id': o1.location_id.id, 'location_dest_id': o1.location_dest_id.id})]}), 'contenido no se puede')
else:
    skip('08 OUT congelado', 'no hay OUT reservadas con SO')
oser = outs.filtered(lambda p: any(l.product_id.tracking == 'serial' and l.quantity for l in p.move_line_ids))[:1]
if oser:
    run('09 OUT con serie pide captura (almacén)', lambda: oser.with_user(alm).button_validate(),
        lambda r: isinstance(r, dict) and r.get('res_model') == 'almx.serial.confirm.wizard')
else:
    skip('09 OUT con serie', 'no hay OUT reservadas con producto serializado')
unpaid = outs.filtered('not_validate')[:1]
if unpaid:
    run('10 OUT Refacciones sin pago (almacén)', lambda: unpaid.with_user(alm).button_validate(), 'sin pago confirmado')
else:
    skip('10 OUT sin pago', 'no hay OUT de Refacciones sin pago reservadas')

# --- Pedimento ---
imp = env['stock.picking'].search([('picking_type_code', '=', 'incoming'), ('state', '=', 'assigned'),
                                   ('purchase_id.almx_is_import', '=', True), ('entry_number', '=', False)], limit=1)
if imp:
    run('11 IN importación sin pedimento', lambda: imp.with_user(alm).button_validate(), 'Captura el número de pedimento')
    run('12 Pedimento con formato inválido', lambda: imp.with_user(alm).write({'entry_number': 'ABC123'}), 'no es un número de pedimento válido')
    run('13 Pedimento se normaliza', lambda: (imp.with_user(alm).write({'entry_number': '26431925-6000244'}), imp.entry_number)[1],
        lambda r: r == '26 43 1925 6000244')
else:
    skip('11-13 Pedimento', 'no hay recepciones de importación pendientes')


# --- Vista y datos ---
def buttons():
    arch = env['stock.picking'].get_views([(False, 'form')])['views']['form']['arch']
    return re.findall(r'<button[^>]*name="button_validate"[^>]*>', arch)


btns = buttons()
run('14 Botón Validar: 2 botones, ocultos por estado y por pago', lambda: btns,
    lambda r: len(r) == 2 and all('state' in b and 'not_validate' in b for b in r))


def mirror():
    env.cr.execute("""select count(*) from stock_picking sp join sale_order so on so.id = sp.sale_id
                      where sp.x_studio_tipo_de_venta is distinct from so.sale_type
                         or coalesce(sp.x_studio_completamente_pagado, false) <> coalesce(so.completely_paid, false)""")
    return env.cr.fetchone()[0]


run('15 Tipo de venta / Venta pagada en traslados = SO (diferencias)', mirror, lambda r: r == 0)

# --- Ventas ---
so_c = env['sale.order'].search([('state', '=', 'sale'), ('sale_type', '!=', False), ('user_id', '!=', False)],
                                order='id desc', limit=50).filtered(lambda s: not s.user_id.has_group('almx_sale.group_so_admin'))[:1]
if so_c:
    vend = so_c.user_id
    run('16 Cambiar Tipo de venta en SO confirmada (%s)' % vend.login, lambda: so_c.with_user(vend).write(
        {'sale_type': 'project' if so_c.sale_type != 'project' else 'spare'}), 'no se puede modificar')
    run('17 Cancelar SO (%s)' % vend.login, lambda: so_c.with_user(vend).action_cancel(), 'Solo el área de TI')

    def so_sin_tipo():
        so = env['sale.order'].with_user(vend).create({'partner_id': so_c.partner_id.id, 'order_line': [
            (0, 0, {'product_id': so_c.order_line.product_id[:1].id, 'product_uom_qty': 1})]})
        return so.action_confirm()

    run('18 Confirmar SO sin Tipo de venta (%s)' % vend.login, so_sin_tipo, 'Indica el Tipo de venta')
else:
    skip('16-18 Ventas', 'no hay SO confirmadas de vendedores fuera de TI')

# --- Devoluciones (informativo: revisar destino) ---
od = env['stock.picking'].search([('picking_type_id', '=', OUT.id), ('state', '=', 'done'),
                                  ('move_ids.move_orig_ids', '!=', False)], order='id desc', limit=1)


def devol():
    w = env['stock.return.picking'].with_context(active_id=od.id, active_ids=od.ids,
                                                 active_model='stock.picking').create({'picking_id': od.id})
    for line in w.product_return_moves:
        line.quantity = 1
    res = w.action_create_returns()
    newp = env['stock.picking'].browse(res['res_id'])
    return '%s | origen PICK: %s | destino devolución: %s' % (
        od.name, od.move_ids.move_orig_ids.location_id.mapped('complete_name')[:2],
        newp.move_ids.location_dest_id.mapped('complete_name'))


if od:
    run('19 Devolución de OUT: destino', devol, None)

env.cr.rollback()
print('Usuarios: almacén=%s | Dirección=%s (grupo: %s) | Producto: %s @ %s' % (
    alm.login, hamdi.login, ', '.join(DIR.mapped('login')), prod.display_name, src.complete_name))
for s, n, d in R:
    print('%-5s %-60s %s' % (s, n, d))
print('Botones Validar:')
for b in btns:
    print('   ' + b)
print('Resumen: %d OK, %d FALLA, %d INFO, %d S/C  -- todo revertido (rollback)' % tuple(
    sum(1 for r in R if r[0] == k) for k in ('OK', 'FALLA', 'INFO', 'S/C')))
