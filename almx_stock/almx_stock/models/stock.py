# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_in_group = fields.Boolean(string='Pertenece al grupo??', help='Valida si el movimiento de almacén actual es un PICK', compute='pick_validation_confirm')
    collect_date = fields.Datetime(string='Fecha de recolección', help='Fecha de recolección elegida para una recolección programada', tracking=True)
    carrier_id = fields.Many2one('delivery.carrier', string='Método de entrega', help='Método de entrega elegido para la orden de venta', tracking=True)
    is_immediate = fields.Boolean(string='Es entrega inmediata?', help='Muestra si la órden de venta está configurada para entrega inmediata', compute='get_sale_values')
    is_paid = fields.Boolean(string='Pagado', help='Verifica si la orden de venta que generó el movimiento de almacén se encuentra pagada', tracking=True)
    is_account_manager = fields.Boolean(string='Pertenece a contabilidad?', help='Verifica si la orden de venta que generó el movimiento de almacén se encuentra pagada', compute='is_in_group_validation')
    # ALMX FIX (sept 2026, port a 19): se quitaron warehouse_already/store_already/
    # lab_already/quality_already (+ sus _date y _check) -- "Material listo" por
    # departamento. Confirmado con el usuario que no funcionaban de verdad en 16
    # (no bloqueaban nada, no se usaban), limpieza acordada explicitamente.
    out_complement = fields.Char(string='OUT complemento', help='Muestra los complementos del OUT')
    partner_receives = fields.Char(string='Persona que recibe')
    not_validate = fields.Boolean(string='No se puede validar', help='Muestra si la condición de pagado aplica para la orden de venta relacionada al movimiento de almacén actual', compute='compute_spare_sale_order')
    # ALMX FIX (19.0 compat, sept 2026): x_studio_tipo_de_venta y
    # x_studio_completamente_pagado eran campos de Studio en 16 (nunca definidos
    # en codigo por ningun modulo) que no sobrevivieron el upgrade de base de
    # datos a 19. Se recrean aqui como campos propios del modulo, consolidado
    # con not_validate/compute_spare_sale_order, que es lo unico que los usa.
    x_studio_tipo_de_venta = fields.Selection(related='sale_id.sale_type', string='Tipo de venta', store=True)
    # x_studio_completamente_pagado: NO es related directo (a diferencia de
    # arriba) porque completely_paid en sale.order esta restringido al grupo
    # de Finanzas (almx_sale.group_can_confirm_sale_payment). Un related
    # normal hereda esa restriccion al intentar leer el campo origen, y
    # Almacen dejaria de poder consultar el estado de pago en el OUT (que es
    # justo lo que se pidio que SI pudieran hacer, solo sin editar). Con un
    # compute + sudo() se lee el valor saltandose esa restriccion puntual,
    # y el campo se queda de solo lectura para todos por no tener inverse.
    x_studio_completamente_pagado = fields.Boolean(string='Completamente pagado', compute='_compute_completamente_pagado', store=True)

    # ALMX (sept 2026, port a 19): URLs de evidencia fotográfica. En 16 eran
    # campos de Studio (x_studio_*) mostrados por una vista de Studio que no
    # sobrevivió la migración; los campos y sus datos SÍ llegaron a 19 como
    # campos manuales. Se declaran aquí con el mismo nombre técnico para que
    # dejen de depender de Studio (misma columna, no se pierde información).
    # Se conservan los 4 porque no está claro en qué momento se usa cada uno.
    x_studio_evidencia_fotogrfica = fields.Char(
        string='URL Almacén',
        help='Enlace de Google Drive con las fotografías de evidencia de esta transferencia.')
    x_studio_url_bodega = fields.Char(string='URL Bodega')
    x_studio_url_laboratorio = fields.Char(string='URL Laboratorio')
    x_studio_url_calidad = fields.Char(string='URL Calidad')
    # Boolean de Studio sin uso desde 2023 y sin vista en 16; se declara solo
    # para conservar el histórico, no se muestra.
    x_studio_adir_evidencia = fields.Boolean(string='Añadir Evidencia')

    @api.depends('sale_id.completely_paid')
    def _compute_completamente_pagado(self):
        for rec in self:
            rec.x_studio_completamente_pagado = rec.sudo().sale_id.completely_paid
    show_request_authorization = fields.Boolean(
        string='Mostrar botón de solicitar autorización',
        compute='_compute_show_request_authorization',
        help='True si el usuario actual NO pertenece al grupo autorizado '
             'para validar pickings (almx_stock.group_can_validate_picking_doppler, NWH) '
             'y el picking es una salida (outgoing). '
             'Controla la visibilidad del botón "Solicitar autorización" en la vista.'
    )
    #PC Fields
    partner_only_dir = fields.Many2one('res.partner', string="Dirección de entrega")
    address_display = fields.Char(string='Dirección completa', compute='_compute_address_display', store=False,
        help='Dirección completa (calle, ciudad, estado, CP, país) del contacto de entrega. '
             'Se calcula a partir de partner_only_dir si tiene valor, o de partner_id en su defecto. '
             'Solo expone campos de dirección, nunca nombre/teléfono/otros datos del contacto.')

    @api.depends(
        'partner_only_dir', 'partner_only_dir.street', 'partner_only_dir.street2',
        'partner_only_dir.city', 'partner_only_dir.state_id', 'partner_only_dir.zip',
        'partner_only_dir.country_id',
        'partner_id', 'partner_id.street', 'partner_id.street2', 'partner_id.city',
        'partner_id.state_id', 'partner_id.zip', 'partner_id.country_id',
    )
    def _compute_address_display(self):
        for rec in self:
            partner = rec.partner_only_dir or rec.partner_id
            if not partner:
                rec.address_display = False
                continue
            parts = []
            if partner.street:
                parts.append(partner.street)
            if partner.street2:
                parts.append(partner.street2)
            city_state = ', '.join(filter(None, [partner.city, partner.state_id.name if partner.state_id else False]))
            if city_state:
                parts.append(city_state)
            if partner.zip:
                parts.append(partner.zip)
            if partner.country_id:
                parts.append(partner.country_id.name)
            rec.address_display = ', '.join(parts) if parts else False

    def button_validate(self):
        #Verificamos que pertenezca o nó al grupo de validación Manual.
        #1- Si no esta en el grupo puede validar operaciones manuales
        if not self.env.user.has_group('almx_stock.no_validate_manual_picking'):
            return super(StockPicking, self).button_validate()
            
        #2- Aunque esté en el grupo, si es un picking desde un pedido, si puede validarlo
        elif self.env.user.has_group('almx_stock.no_validate_manual_picking') and self.sale_id:
            return super(StockPicking, self).button_validate()
        else:
            raise ValidationError(_("Es necesario solicitar la validación del PICK con tu lider o dirección, ya que no cuentas con permisos suficientes."))

    @api.depends('is_in_group')
    def pick_validation_confirm(self):
        for rec in self:
            pick_name = rec.picking_type_id.name
            #Si el usuario NO pertenece al grupo de Validar PICK, el movimiento está en borrador y es un pick
            if self.env.user.has_group('almx_stock.no_validate_manual_picking') and rec.state in ('draft','waiting') and pick_name == "Picking":
                rec.is_in_group = False
            else:
                rec.is_in_group = True

    def get_sale_values(self):
        for rec in self:
            stock = rec
            carrier = stock.sale_id.carrier_id.id
            collect_date = stock.sale_id.collect_date
            if carrier:
                rec.carrier_id = carrier
                rec.is_immediate = True
            else:
                rec.is_immediate = False
            if collect_date:
                collect_date_new = collect_date.strftime('%d/%m/%Y %H:%M:%S')
                rec.collect_date = collect_date
                rec.is_immediate = True
            else:
                rec.is_immediate = False

    def is_in_group_validation(self):
        if self.env.user.has_group('account.group_account_manager'):
            self.is_account_manager = True
        else:
            self.is_account_manager = False

    def compute_spare_sale_order(self):
        for rec in self:
            op_type = rec.picking_type_id.id
            sale_type = rec.x_studio_tipo_de_venta
            comp_paid = rec.x_studio_completamente_pagado
            if sale_type == 'spare' and comp_paid != True and op_type == 37: #Aplica solo para movimientos que son OUT
                rec.not_validate = True
            else:
                rec.not_validate = False

    def _get_authorized_validators(self):
        """ Usuarios que hoy pueden validar pickings (grupo de Doppler/NWH).
        Se usa SOLO para decidir si mostrar el botón "Solicitar autorización"
        (se muestra a quien NO esté aquí). No es la lista de a quién se notifica;
        ver _get_authorization_notify_recipients para eso.

        ALMX FIX (sept 2026, port a 19): antes tambien se consultaba
        doppler.group_can_validate_picking_alamex (almacen WH/Alamex). Se dejo
        de usar ese almacen, asi que ese grupo no se recreo al portar a 19
        (decision de negocio, no un pendiente tecnico). """
        doppler_group = self.env.ref('almx_stock.group_can_validate_picking_doppler', raise_if_not_found=False)
        validators = self.env['res.users']
        if doppler_group:
            validators |= doppler_group.user_ids
        return validators

    def _get_authorization_notify_recipients(self):
        """ A quién se le avisa cuando alguien pide autorización. Deliberadamente
        separado de _get_authorized_validators: no todo el que puede validar debe
        recibir cada solicitud (ej. administradores que no dan seguimiento operativo
        diario de almacén). Se administra en Ajustes > Grupos >
        "Recibe solicitudes de autorización de PICK". """
        notify_group = self.env.ref('almx_stock.group_picking_authorization_notify', raise_if_not_found=False)
        return notify_group.users if notify_group else self.env['res.users']

    @api.depends('picking_type_code')
    def _compute_show_request_authorization(self):
        validators = self._get_authorized_validators()
        is_authorized = self.env.user in validators
        for picking in self:
            picking.show_request_authorization = (
                picking.picking_type_code == 'outgoing' and not is_authorized
            )

    def action_request_validation_authorization(self):
        """ Notifica en el chatter del picking a los usuarios configurados para
        recibir solicitudes de autorización (grupo group_picking_authorization_notify),
        pidiendo que revisen y validen este PICK manualmente. """
        self.ensure_one()
        recipients = self._get_authorization_notify_recipients()
        if not recipients:
            raise UserError(_(
                "No hay ningún usuario configurado actualmente para recibir "
                "solicitudes de autorización. Contacta a tu administrador."
            ))
        partners = recipients.mapped('partner_id')
        self.message_post(
            body=_(
                "🔔 %(solicitante)s solicita autorización para validar este PICK "
                "(%(picking)s). Por favor revisa y valida si corresponde."
            ) % {'solicitante': self.env.user.name, 'picking': self.name},
            partner_ids=partners.ids,
        )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Solicitud enviada'),
                'message': _('Se notificó a %d persona(s) autorizada(s) para validar este PICK.') % len(recipients),
                'type': 'success',
                'sticky': False,
            }
        }