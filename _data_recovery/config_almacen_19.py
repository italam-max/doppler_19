# -*- coding: utf-8 -*-
"""
_data_recovery/config_almacen_19.py
===================================
Activa en 19 los candados de almacén. almx_stock_movement_guard y
almx_serial_verification funcionan con banderas en tipos de operación y
ubicaciones que los módulos no traen en datos (en el ensayo se pusieron a mano
y se perdieron con el proyecto alamex-elevetors2).

Decisiones (1-nov-2026):
  - SO obligatoria: NWH/PICK, NWH/OUT y DPGDL/OUT
  - Congelar contenido: solo los OUT (el PICK no: Laboratorio agrega material)
  - Confirmar número de serie: NWH/OUT y DPGDL/OUT
  - Candado de recepciones (sin PO ni devolución nativa -> Dirección): IN y RET de NWH y DPGDL
  - Solo Dirección: Merma, Stock Laboratorio, Banco de Pruebas, LABORATORIO CONSUMO,
    Descarte y Desecho, WHTL/Scrap (incluye sububicaciones)
  - Asignación de equipo: pendiente, no se configura

Idempotente. Uso (shell de Odoo.sh, desde la carpeta del repo):
  DRY_RUN=1 odoo-bin shell --no-http < _data_recovery/config_almacen_19.py
  odoo-bin shell --no-http < _data_recovery/config_almacen_19.py
"""
import os

DRY = os.environ.get('DRY_RUN') == '1'
ok, warn = [], []

OUT = {'almx_require_sale_order': True, 'almx_freeze_lines': True, 'require_serial_confirmation': True}
REC = {'almx_guard_receipts': True}
TYPES = [
    ('WHTl', 'NWH/PICK/', {'almx_require_sale_order': True}),
    ('WHTl', 'NWH/OUT/', OUT),
    ('DPGDL', 'OUT', OUT),
    ('WHTl', 'NWH/IN/', REC),
    ('WHTl', 'RET', REC),
    ('DPGDL', 'IN', REC),
    ('DPGDL', 'RET', REC),
]
for wh, seq, vals in TYPES:
    t = env['stock.picking.type'].search([('warehouse_id.code', '=', wh), ('sequence_code', '=', seq)])
    if len(t) != 1:
        warn.append('tipo no encontrado o duplicado: %s %s (%d)' % (wh, seq, len(t)))
        continue
    diff = {k: v for k, v in vals.items() if t[k] != v}
    if diff and not DRY:
        t.write(diff)
    ok.append('tipo %-6s %-10s %s' % (wh, seq, ', '.join(sorted(diff)) or 'sin cambios'))

LOCS = [(376, 'merma'), (3612, 'laboratorio'), (3616, 'banco de pruebas'),
        (3629, 'laboratorio consumo'), (3613, 'desecho'), (1050, 'whtl/scrap')]
for lid, key in LOCS:
    loc = env['stock.location'].browse(lid).exists()
    if not loc or key not in loc.complete_name.lower():
        warn.append('ubicación %s no coincide (%s)' % (lid, loc.complete_name if loc else 'no existe'))
        continue
    changed = not loc.almx_requires_direction
    if changed and not DRY:
        loc.almx_requires_direction = True
    ok.append('Dirección: %s (%s)' % (loc.complete_name, 'activada' if changed else 'sin cambios'))

if DRY:
    env.cr.rollback()
else:
    env.cr.commit()
print('[%s]' % ('DRY_RUN' if DRY else 'APLICADO'))
print('\n'.join(ok))
print('\n'.join('AVISO: ' + w for w in warn) or 'sin avisos')
