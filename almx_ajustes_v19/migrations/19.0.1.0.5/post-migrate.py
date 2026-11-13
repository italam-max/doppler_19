"""Pasa las Evaluaciones psicológicas de los campos de Studio (16) a los campos del módulo.

Reasigna res_field de cada adjunto al campo nuevo y copia el nombre de archivo.
Solo mueve los adjuntos con archivo físico en el filestore; los perdidos en la
migración 13 -> 16 se quedan en el campo de Studio (se depreciará después).
Idempotente: se puede correr más de una vez.
"""
import logging
import os

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

# campo Studio -> campo del módulo
FIELD_MAP = {
    "x_studio_field_rNDk8": "almx_machover",
    "x_studio_field_UpoqW": "almx_man_in_rain",
    "x_studio_field_LJGRB": "almx_zavic",
    "x_studio_field_2kQbH": "almx_psychometric_test",
}


def _column_exists(cr, table, column):
    cr.execute(
        "SELECT 1 FROM information_schema.columns WHERE table_name=%s AND column_name=%s",
        (table, column),  # Odoo crea las columnas de Studio respetando mayúsculas
    )
    return bool(cr.fetchone())


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Attachment = env["ir.attachment"]
    moved = skipped = 0

    for old, new in FIELD_MAP.items():
        old_fname = f"{old}_filename"
        has_fname_col = _column_exists(cr, "hr_applicant", old_fname)

        atts = Attachment.search([("res_model", "=", "hr.applicant"), ("res_field", "=", old)])
        for att in atts:
            has_file = bool(att.db_datas) or (
                att.store_fname and os.path.isfile(att._full_path(att.store_fname))
            )
            if not has_file:
                skipped += 1
                continue
            # si el candidato ya tiene archivo en el campo nuevo, no se pisa
            cr.execute(
                "SELECT 1 FROM ir_attachment WHERE res_model='hr.applicant' "
                "AND res_field=%s AND res_id=%s",
                (new, att.res_id),
            )
            if cr.fetchone():
                continue
            cr.execute(
                "UPDATE ir_attachment SET res_field=%s, name=%s WHERE id=%s",
                (new, new, att.id),
            )
            if has_fname_col:
                cr.execute(
                    f'UPDATE hr_applicant SET "{new}_filename" = "{old_fname}" WHERE id=%s',
                    (att.res_id,),
                )
            moved += 1

    # IQ (entero, sin adjunto)
    if _column_exists(cr, "hr_applicant", "x_studio_field_M2s7A"):
        cr.execute(
            'UPDATE hr_applicant SET almx_iq = "x_studio_field_M2s7A" '
            'WHERE almx_iq IS NULL AND "x_studio_field_M2s7A" IS NOT NULL'
        )
        _logger.info("almx_ajustes_v19: IQ copiado en %s candidatos", cr.rowcount)

    env.invalidate_all()
    _logger.info(
        "almx_ajustes_v19: evaluaciones psicológicas migradas=%s, sin archivo (omitidas)=%s",
        moved, skipped,
    )
