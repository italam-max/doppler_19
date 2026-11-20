from odoo import _, api, fields, models
from odoo.exceptions import UserError

PAQUETERIAS = [
    ('tres_guerras', 'Tres Guerras'),
    ('paquete_express', 'Paquete Express'),
    ('castores', 'Castores'),
    ('etn', 'ETN'),
    ('otra', 'Otra'),
]
TIPOS_SERVICIO = [('domicilio', 'A domicilio'), ('ocurre', 'Ocurre (sucursal)')]
APPS = [('uber', 'Uber'), ('didi', 'DiDi'), ('otra', 'Otra')]
FISCAL_REQUIRED = ('tres_guerras', 'castores')
ADDRESS_KINDS = ('paqueteria', 'flete')
LEGACY_RECOLECCION_NAME = 'Recolección Programada'
# El flujo de envío (ventanas, datos obligatorios y bloqueo de campos) solo aplica a ventas de Refacciones.
SHIPPING_FLOW_SALE_TYPE = 'spare'

# Campos que aplica cada tipo de método; los demás se limpian.
KIND_FIELDS = {
    'paqueteria': ('almx_paqueteria', 'almx_paqueteria_otra', 'almx_tipo_servicio', 'almx_sucursal_destino'),
    'flete': ('almx_contacto_nombre', 'almx_contacto_telefono'),
    'app': ('almx_app_servicio', 'almx_app_otra', 'almx_app_referencia'),
}
ALL_SHIPPING_FIELDS = tuple(f for fs in KIND_FIELDS.values() for f in fs)


def almx_shipping_core_missing(rec, kind, sale_type):
    """Datos propios del método (sin dirección ni datos fiscales). Sirve para la venta y para la ventana."""
    missing = []
    if kind == 'paqueteria':
        if not rec.almx_paqueteria:
            missing.append(_('Paquetería'))
        elif rec.almx_paqueteria == 'otra' and not rec.almx_paqueteria_otra:
            missing.append(_('Nombre de la otra paquetería'))
        if not rec.almx_tipo_servicio:
            missing.append(_('Tipo de servicio (a domicilio u ocurre)'))
    elif kind == 'flete':
        if not rec.almx_contacto_nombre:
            missing.append(_('Contacto de entrega'))
        if not rec.almx_contacto_telefono:
            missing.append(_('Teléfono de contacto'))
    elif kind == 'recoleccion':
        if not rec.collect_date:
            missing.append(_('Fecha y hora de recolección'))
    elif kind == 'app':
        if not rec.almx_app_servicio:
            missing.append(_('App de envío'))
        elif rec.almx_app_servicio == 'otra' and not rec.almx_app_otra:
            missing.append(_('Nombre de la otra app'))
        if not rec.almx_app_referencia:
            missing.append(_('Referencia o placas'))
    elif kind == 'proyecto' and sale_type != 'project':
        missing.append(_('El método Proyecto Alamex solo aplica a ventas de Equipo Nuevo'))
    return missing


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    almx_shipping_kind = fields.Selection(related='carrier_id.almx_shipping_kind', string='Tipo de método')
    almx_paqueteria = fields.Selection(PAQUETERIAS, string='Paquetería', tracking=True)
    almx_paqueteria_otra = fields.Char(string='Otra paquetería', tracking=True)
    almx_tipo_servicio = fields.Selection(TIPOS_SERVICIO, string='Tipo de servicio', tracking=True)
    almx_sucursal_destino = fields.Char(string='Sucursal destino', tracking=True)
    almx_contacto_nombre = fields.Char(string='Contacto de entrega', tracking=True)
    almx_contacto_telefono = fields.Char(string='Teléfono de contacto', tracking=True)
    almx_app_servicio = fields.Selection(APPS, string='App de envío', tracking=True)
    almx_app_otra = fields.Char(string='Otra app', tracking=True)
    almx_app_referencia = fields.Char(string='Referencia / placas', tracking=True)

    # Reemplaza el onchange de almx_sale, que comparaba el nombre exacto del método.
    @api.onchange('carrier_id')
    def is_immediate_carrier(self):
        for order in self:
            carrier = order.carrier_id
            kind = carrier.almx_shipping_kind
            order.is_immediate = kind == 'recoleccion' or (not kind and carrier.name == LEGACY_RECOLECCION_NAME)
            if not order.is_immediate:
                order.collect_date = False
            keep = KIND_FIELDS.get(kind, ())
            for fname in ALL_SHIPPING_FIELDS:
                if fname not in keep and order[fname]:
                    order[fname] = False

    # --- Ventanas -------------------------------------------------------------------------------
    def _almx_wizard_action(self, model, name, extra_ctx=None):
        self.ensure_one()
        if self.sale_type != SHIPPING_FLOW_SALE_TYPE:
            raise UserError(_('Estas ventanas solo aplican a ventas de Refacciones.'))
        ctx = {'default_order_id': self.id}
        ctx.update(extra_ctx or {})
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': model,
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
        }

    def action_almx_open_shipping_wizard(self, confirm_after=False):
        return self._almx_wizard_action('almx.shipping.method.wizard', _('Método de envío'),
                                        {'almx_confirm_after': bool(confirm_after)})

    def action_almx_open_address_wizard(self):
        return self._almx_wizard_action('almx.shipping.address.wizard', _('Dirección de entrega'))

    def action_almx_open_fiscal_wizard(self):
        return self._almx_wizard_action('almx.fiscal.data.wizard', _('Datos de facturación'))

    # --- Validación al confirmar -----------------------------------------------------------------
    def _almx_missing_address(self):
        self.ensure_one()
        address = self.partner_shipping_id
        if not address:
            return [_('Dirección de entrega')]
        missing = []
        if not address.street:
            missing.append(_('Calle y número de la dirección de entrega'))
        if not address.zip:
            missing.append(_('C.P. de la dirección de entrega'))
        if not address.city and not address.state_id:
            missing.append(_('Ciudad o estado de la dirección de entrega'))
        return missing

    def _almx_missing_fiscal(self):
        self.ensure_one()
        partner = self.partner_id.commercial_partner_id
        missing = []
        if not partner.name:
            missing.append(_('Razón social del cliente'))
        if not partner.vat:
            missing.append(_('RFC del cliente'))
        if not partner.l10n_mx_edi_fiscal_regime:
            missing.append(_('Régimen fiscal del cliente'))
        if not partner.zip:
            missing.append(_('C.P. fiscal del cliente'))
        return missing

    def _almx_shipping_problems(self, require_carrier=False):
        problems = []
        for order in self:
            if order.sale_type != SHIPPING_FLOW_SALE_TYPE:
                continue
            if not order.carrier_id:
                if require_carrier:
                    problems.append((order, [_('Método de envío')]))
                continue
            kind = order.carrier_id.almx_shipping_kind
            if not kind:
                continue
            missing = almx_shipping_core_missing(order, kind, order.sale_type)
            if kind in ADDRESS_KINDS:
                missing += order._almx_missing_address()
            if kind == 'paqueteria' and order.almx_paqueteria in FISCAL_REQUIRED:
                missing += order._almx_missing_fiscal()
            if missing:
                problems.append((order, missing))
        return problems

    def _almx_check_shipping_data(self, require_carrier=False):
        problems = self._almx_shipping_problems(require_carrier)
        if problems:
            raise UserError(_('No se puede confirmar la venta. Falta información del método de envío:\n\n%s') % '\n\n'.join(
                '%s (%s):\n%s' % (order.name, order.carrier_id.name or _('sin método'),
                                  '\n'.join('• %s' % m for m in missing))
                for order, missing in problems))

    def _action_confirm(self):
        res = super()._action_confirm()
        self.picking_ids._almx_sync_carrier_from_sale()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'carrier_id' in vals:
            self.picking_ids._almx_sync_carrier_from_sale()
        return res

    def action_confirm(self):
        from_ui = self.env.context.get('almx_confirm_ui')
        # Desde el botón Confirmar: si falta algo, se abre la ventana para completarlo en lugar de un error.
        if from_ui and len(self) == 1 and self._almx_shipping_problems(require_carrier=True):
            return self.action_almx_open_shipping_wizard(confirm_after=True)
        self._almx_check_shipping_data(require_carrier=bool(from_ui))
        return super().action_confirm()
