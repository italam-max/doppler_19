import re

from odoo import _, fields, models

RFC_RE = re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$')
ZIP_RE = re.compile(r'^\d{5}$')


class AlmxAddressCaptureMixin(models.AbstractModel):
    _name = 'almx.address.capture.mixin'
    _description = 'Captura de dirección de entrega (Alamex)'

    addr_commercial_id = fields.Many2one('res.partner', string='Cliente')
    addr_mode = fields.Selection(
        [('existing', 'Usar una dirección guardada'), ('new', 'Capturar una dirección nueva')],
        string='Dirección de entrega', default='existing')
    addr_partner_id = fields.Many2one(
        'res.partner', string='Dirección guardada',
        domain="['|', ('id', '=', addr_commercial_id), '&', ('parent_id', '=', addr_commercial_id), ('type', '=', 'delivery')]")
    addr_display = fields.Char(related='addr_partner_id.contact_address', string='Dirección completa')
    addr_name = fields.Char(string='Nombre / quién recibe')
    addr_street_name = fields.Char(string='Calle')
    addr_street_number = fields.Char(string='Número exterior')
    addr_street_number2 = fields.Char(string='Número interior')
    addr_colony = fields.Char(string='Colonia')
    addr_city = fields.Char(string='Ciudad o municipio')
    addr_state_id = fields.Many2one('res.country.state', string='Estado', domain="[('country_id.code', '=', 'MX')]")
    addr_zip = fields.Char(string='C.P.')
    addr_phone = fields.Char(string='Teléfono de quien recibe')
    addr_reference = fields.Char(string='Referencias')

    def _addr_defaults(self, order):
        return {
            'addr_commercial_id': order.partner_id.commercial_partner_id.id,
            'addr_mode': 'existing',
            'addr_partner_id': order.partner_shipping_id.id,
        }

    def _addr_missing(self):
        self.ensure_one()
        if self.addr_mode == 'existing':
            address = self.addr_partner_id
            if not address:
                return [_('Elige una dirección de entrega guardada o captura una nueva')]
            missing = []
            if not address.street:
                missing.append(_('La dirección guardada no tiene calle y número'))
            if not address.zip:
                missing.append(_('La dirección guardada no tiene C.P.'))
            if not address.city and not address.state_id:
                missing.append(_('La dirección guardada no tiene ciudad ni estado'))
            if missing:
                missing.append(_('Captura una dirección nueva con los datos completos'))
            return missing
        checks = [
            (self.addr_name, _('Nombre / quién recibe')),
            (self.addr_street_name, _('Calle')),
            (self.addr_street_number, _('Número exterior')),
            (self.addr_colony, _('Colonia')),
            (self.addr_city, _('Ciudad o municipio')),
            (self.addr_state_id, _('Estado')),
            (self.addr_zip, _('C.P.')),
        ]
        missing = [label for value, label in checks if not value]
        if self.addr_zip and not ZIP_RE.match(self.addr_zip.strip()):
            missing.append(_('El C.P. de entrega debe tener 5 dígitos'))
        return missing

    def _addr_resolve(self):
        """Dirección guardada, o una dirección de entrega nueva hija del cliente. Nunca toca la dirección fiscal."""
        self.ensure_one()
        if self.addr_mode == 'existing':
            return self.addr_partner_id
        state = self.addr_state_id
        return self.env['res.partner'].with_context(almx_partner_wizard=True).create({
            'type': 'delivery',
            'parent_id': self.addr_commercial_id.id,
            'name': self.addr_name.strip(),
            'street_name': self.addr_street_name.strip(),
            'street_number': self.addr_street_number.strip(),
            'street_number2': (self.addr_street_number2 or '').strip() or False,
            'l10n_mx_edi_colony': self.addr_colony.strip(),
            'city': self.addr_city.strip(),
            'state_id': state.id,
            'country_id': state.country_id.id,
            'zip': self.addr_zip.strip(),
            'phone': self.addr_phone or False,
            'comment': self.addr_reference or False,
        })


class AlmxFiscalCaptureMixin(models.AbstractModel):
    _name = 'almx.fiscal.capture.mixin'
    _description = 'Captura de datos fiscales del cliente (Alamex)'

    fis_partner_id = fields.Many2one('res.partner', string='Cliente (razón social)')
    fis_name = fields.Char(string='Razón social')
    fis_vat = fields.Char(string='RFC')
    fis_regime = fields.Selection(
        selection=lambda self: self.env['res.partner']._fields['l10n_mx_edi_fiscal_regime']._description_selection(self.env),
        string='Régimen fiscal')
    fis_zip = fields.Char(string='C.P. fiscal')
    fis_csf = fields.Binary(string='Constancia de situación fiscal (CSF)')
    fis_csf_filename = fields.Char(string='Nombre del archivo CSF')

    def _fis_defaults(self, partner):
        partner = partner.commercial_partner_id
        return {
            'fis_partner_id': partner.id,
            'fis_name': partner.name,
            'fis_vat': partner.vat,
            'fis_regime': partner.l10n_mx_edi_fiscal_regime,
            'fis_zip': partner.zip,
        }

    def _fis_missing(self):
        self.ensure_one()
        missing = []
        if not (self.fis_name or '').strip():
            missing.append(_('Razón social'))
        vat = (self.fis_vat or '').strip().upper()
        if not vat:
            missing.append(_('RFC'))
        elif not RFC_RE.match(vat):
            missing.append(_('El RFC no tiene un formato válido (12 o 13 caracteres, sin guiones ni espacios)'))
        if not self.fis_regime:
            missing.append(_('Régimen fiscal'))
        zip_code = (self.fis_zip or '').strip()
        if not zip_code:
            missing.append(_('C.P. fiscal'))
        elif not ZIP_RE.match(zip_code):
            missing.append(_('El C.P. fiscal debe tener 5 dígitos'))
        return missing

    def _fis_apply(self):
        self.ensure_one()
        partner = self.fis_partner_id.commercial_partner_id
        new = {
            'name': self.fis_name.strip(),
            'vat': self.fis_vat.strip().upper(),
            'l10n_mx_edi_fiscal_regime': self.fis_regime,
            'zip': self.fis_zip.strip(),
        }
        # Solo se escribe lo que cambió de verdad (ignorando espacios y mayúsculas del RFC), para no disparar
        # validaciones del contacto por diferencias que no son cambios.
        vals = {k: v for k, v in new.items() if (partner[k] or '').strip() != v}
        if self.fis_csf:
            vals.update({'csf_document': self.fis_csf, 'csf_document_filename': self.fis_csf_filename})
        if vals:
            partner.with_context(almx_partner_wizard=True).write(vals)
