# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AlmxSerialConfirmWizard(models.TransientModel):
    _name = 'almx.serial.confirm.wizard'
    _description = 'Confirmación manual de números de serie antes de validar'

    picking_ids = fields.Many2many('stock.picking', string='Traslados')
    line_ids = fields.One2many(
        'almx.serial.confirm.wizard.line', 'wizard_id', string='Productos por confirmar'
    )

    def action_confirm_and_validate(self):
        """La validez se recalcula aquí, server-side, desde la serie elegida:
        no se confía en lo que calculó el onchange en el navegador."""
        self.ensure_one()

        results = {}
        for line in self.line_ids:
            lot, quant, message = line._almx_verify()
            results[line.id] = (lot, quant, message)
            line.write({
                'matched_lot_id': lot.id if lot else False,
                'is_valid': bool(lot),
                'validation_message': message,
            })

        invalid = self.line_ids.filtered(lambda l: not results[l.id][0])
        if invalid:
            details = '\n'.join(
                '- %s: %s' % (l.product_id.display_name, results[l.id][2]) for l in invalid
            )
            raise UserError(_(
                "Todavía hay números de serie sin validar. Selecciona el número "
                "de serie real de cada producto antes de continuar.\n\n%(details)s",
                details=details,
            ))

        entered = [results[l.id][0] for l in self.line_ids]
        if len(entered) != len(set(entered)):
            raise UserError(_("Seleccionaste el mismo número de serie en más de una línea."))

        # Escribir la serie capturada en la línea real. Si es distinta a la
        # reservada, stock.move.line.write() reacomoda la reserva de forma
        # nativa. Se marca 'picked' para que Odoo 19 la procese.
        for line in self.line_ids:
            lot, quant, _msg = results[line.id]
            ml = line.move_line_id
            vals = {'lot_id': lot.id, 'picked': True}
            if quant and quant.location_id != ml.location_id:
                vals['location_id'] = quant.location_id.id
            if ml.product_uom_id.is_zero(ml.quantity):
                vals['quantity'] = 1
            ml.write(vals)

        return self.picking_ids.with_context(almx_serial_confirmed=True).button_validate()


class AlmxSerialConfirmWizardLine(models.TransientModel):
    _name = 'almx.serial.confirm.wizard.line'
    _description = 'Línea de confirmación de número de serie'

    wizard_id = fields.Many2one('almx.serial.confirm.wizard', required=True, ondelete='cascade')
    move_line_id = fields.Many2one('stock.move.line', required=True, readonly=True)
    picking_id = fields.Many2one(related='move_line_id.picking_id', readonly=True)
    product_id = fields.Many2one(related='move_line_id.product_id', readonly=True)
    location_id = fields.Many2one(related='move_line_id.move_id.location_id', readonly=True)

    allowed_lot_ids = fields.Many2many(
        'stock.lot', compute='_compute_allowed_lot_ids',
        string='Series disponibles',
    )
    lot_id = fields.Many2one(
        'stock.lot', string='Número de serie a entregar',
        domain="[('id', 'in', allowed_lot_ids)]",
    )
    matched_lot_id = fields.Many2one('stock.lot', readonly=True)
    is_valid = fields.Boolean(readonly=True, default=False)
    validation_message = fields.Char(string='Estado', readonly=True)

    def _almx_available_quants(self, lot=None):
        """Quants con existencia de este producto en la ubicación origen del
        movimiento (incluye sububicaciones). Si se pasa lot, solo de esa serie."""
        self.ensure_one()
        ml = self.move_line_id
        source = self.location_id or ml.location_id
        company = ml.company_id or self.env.company
        domain = [
            ('product_id', '=', self.product_id.id),
            ('location_id', 'child_of', source.id),
            ('lot_id', '!=', False),
            ('quantity', '>', 0),
            ('company_id', 'in', [company.id, False]),
        ]
        if lot is not None:
            domain.append(('lot_id', '=', lot.id))
        # sudo: stock.quant - solo lectura de existencias para armar la lista
        return self.env['stock.quant'].sudo().search(domain)

    @api.depends('move_line_id')
    def _compute_allowed_lot_ids(self):
        """Series que se pueden entregar: libres en la ubicación origen, más
        la que ya tiene reservada esta misma línea (se ofrece sin distinguirla)."""
        for line in self:
            if not line.move_line_id:
                line.allowed_lot_ids = False
                continue
            quants = line._almx_available_quants()
            lots = quants.filtered(
                lambda q: q.product_uom_id.compare(q.quantity - q.reserved_quantity, 0) > 0
            ).lot_id
            lots |= line.move_line_id.lot_id
            line.allowed_lot_ids = lots.sorted('name')

    def _almx_verify(self):
        """Devuelve (stock.lot, stock.quant, mensaje). lot vacío = inválido.
        quant indica dónde está físicamente la serie (puede ser una
        sububicación distinta a la reservada)."""
        self.ensure_one()
        Lot = self.env['stock.lot']
        Quant = self.env['stock.quant']
        ml = self.move_line_id
        lot = self.lot_id

        if not lot:
            if not self.allowed_lot_ids:
                source = self.location_id or ml.location_id
                return Lot, Quant, _(
                    'No hay números de serie disponibles de este producto en %(loc)s.',
                    loc=source.display_name)
            return Lot, Quant, _('Selecciona un número de serie.')

        if lot.product_id != self.product_id:
            return Lot, Quant, _('El número de serie no corresponde a este producto.')

        # Mismo número que ya tiene reservado esta línea: válido de inmediato.
        if lot == ml.lot_id:
            return lot, Quant, _('Número de serie válido')

        quants = self._almx_available_quants(lot)
        quant = quants.filtered(
            lambda q: q.product_uom_id.compare(q.quantity - q.reserved_quantity, 0) > 0
        )[:1]
        if not quant:
            if quants:
                return Lot, Quant, _(
                    'Ese número de serie está en %(loc)s pero ya está reservado '
                    'para otra operación.', loc=quants[0].location_id.display_name)
            source = self.location_id or ml.location_id
            return Lot, Quant, _(
                'Ese número de serie no tiene existencia disponible en %(loc)s.',
                loc=source.display_name)

        return lot, quant, _('Número de serie válido')

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        """Solo retroalimentación visual; la decisión real se toma en
        action_confirm_and_validate."""
        for line in self:
            lot, _quant, message = line._almx_verify()
            line.matched_lot_id = lot.id if lot else False
            line.is_valid = bool(lot)
            line.validation_message = message if line.lot_id else ''
