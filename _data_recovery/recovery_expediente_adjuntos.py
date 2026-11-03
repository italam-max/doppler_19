# -*- coding: utf-8 -*-
"""
_data_recovery/recovery_expediente_adjuntos.py
==============================================
Liga los documentos del expediente del empleado (filestore de 16) a almx.employee.file (19).
Correr DESPUÉS de recovery_expediente_empleado.sql.

El paquete NO va en el repo (documentos confidenciales de RH). Se arma en el servidor de 16:
  - expediente_adjuntos.tsv: id, res_id, res_field, nombre, mimetype, store_fname
    (ir_attachment con res_model = 'x_hr.employee.file')
  - los archivos del filestore de 16 con su ruta relativa (xx/hash)
se sube a la instancia (editor de Odoo.sh) y se descomprime en EXP_DIR.

  res_field = x_studio_field_FLNyT -> campo 'attachment' del registro
  res_field vacío                  -> adjunto en el chatter del registro
Se omiten archivos que ya no existían en 16 y registros que no se cargaron.
Idempotente. Uso:
  EXP_DIR=~/exp_upload/x DRY_RUN=1 odoo-bin shell --no-http < _data_recovery/recovery_expediente_adjuntos.py
  EXP_DIR=~/exp_upload/x odoo-bin shell --no-http < _data_recovery/recovery_expediente_adjuntos.py
"""
import base64
import os

DRY = os.environ.get('DRY_RUN') == '1'
BASE = os.path.expanduser(os.environ.get('EXP_DIR', '~/exp_upload/x'))
File = env['almx.employee.file'].sudo()
Att = env['ir.attachment'].sudo()
st = dict(campo=0, chatter=0, ya=0, sin_archivo=0, sin_registro=0)

with open(os.path.join(BASE, 'expediente_adjuntos.tsv'), encoding='utf-8') as fh:
    rows = [line.rstrip('\n').split('\t') for line in fh if line.strip()]

for _id, res_id, res_field, name, mimetype, fname in rows:
    rec = File.browse(int(res_id)).exists()
    if not rec:
        st['sin_registro'] += 1
        continue
    path = os.path.join(BASE, fname)
    if not os.path.isfile(path):
        st['sin_archivo'] += 1
        continue
    with open(path, 'rb') as fb:
        raw = fb.read()
    if res_field:
        if rec.attachment:
            st['ya'] += 1
            continue
        if not DRY:
            rec.with_context(tracking_disable=True).write({
                'attachment': base64.b64encode(raw),
                'attachment_filename': rec.attachment_filename or name,
            })
        st['campo'] += 1
    else:
        if Att.search_count([('res_model', '=', File._name), ('res_id', '=', rec.id),
                             ('res_field', '=', False), ('name', '=', name)]):
            st['ya'] += 1
            continue
        if not DRY:
            Att.create({'name': name, 'raw': raw, 'mimetype': mimetype or False,
                        'res_model': File._name, 'res_id': rec.id})
        st['chatter'] += 1

if DRY:
    env.cr.rollback()
else:
    env.cr.commit()
print('[%s] %d filas del paquete' % ('DRY_RUN' if DRY else 'APLICADO', len(rows)))
print('  documento en el registro: %(campo)d | adjunto en chatter: %(chatter)d | ya estaban: %(ya)d' % st)
print('  omitidos: sin archivo en 16 %(sin_archivo)d | registro no cargado %(sin_registro)d' % st)
