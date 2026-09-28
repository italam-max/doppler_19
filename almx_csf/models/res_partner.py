from markupsafe import Markup

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Nombres técnicos conservados desde 16: los adjuntos (ir.attachment) se vuelven a ligar solos.
    csf_document = fields.Binary(string='Constancia de situación fiscal', attachment=True)
    csf_document_filename = fields.Char(string='Nombre del archivo CSF')

    def _almx_csf_log(self, action, name):
        # En 19 message_post escapa el HTML de un str: se usa Markup para que <b> se muestre en negritas.
        msgs = {
            'add': _('El archivo <b>%(name)s</b> fue agregado por %(user)s.'),
            'edit': _('El archivo <b>%(name)s</b> fue modificado por %(user)s.'),
            'delete': _('El archivo <b>%(name)s</b> fue eliminado por %(user)s.'),
        }
        self.message_post(body=Markup(msgs[action]) % {
            'name': name or _('documento'), 'user': self.env.user.name})

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records.filtered('csf_document'):
            record._almx_csf_log('add', record.csf_document_filename)
        return records

    def write(self, vals):
        if 'csf_document' not in vals:
            return super().write(vals)
        previous = {r.id: (bool(r.csf_document), r.csf_document_filename) for r in self}
        has_new = bool(vals.get('csf_document'))
        result = super().write(vals)
        for record in self:
            had_doc, old_name = previous[record.id]
            if has_new:
                record._almx_csf_log('edit' if had_doc else 'add', record.csf_document_filename)
            elif had_doc:
                record._almx_csf_log('delete', old_name)
        return result
