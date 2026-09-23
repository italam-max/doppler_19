import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

PEDIMENTO_RE = re.compile(r'^\s*(\d{2})\s*(\d{2})\s*(\d{4})\s*-?\s*(\d{7})\s*$')


def _normalize_pedimento(value):
    m = PEDIMENTO_RE.match(value or '')
    return ' '.join(m.groups()) if m else value


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    entry_number = fields.Char(
        string='Número de pedimento', copy=False, tracking=True,
        help='Pedimento de importación (15 dígitos: año, aduana, patente, número). '
             'Obligatorio en recepciones de compras de importación.',
    )
    almx_is_import = fields.Boolean(
        string='Compra de importación', compute='_compute_almx_is_import',
    )

    @api.depends('picking_type_code', 'purchase_id.almx_is_import')
    def _compute_almx_is_import(self):
        for picking in self:
            picking.almx_is_import = bool(
                picking.picking_type_code == 'incoming' and picking.purchase_id.almx_is_import)

    # Normaliza al guardar ("26431925-6000244" -> "26 43 1925 6000244")
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('entry_number'):
                vals['entry_number'] = _normalize_pedimento(vals['entry_number'])
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('entry_number'):
            vals['entry_number'] = _normalize_pedimento(vals['entry_number'])
        return super().write(vals)

    @api.constrains('entry_number')
    def _check_entry_number(self):
        for rec in self:
            if not rec.entry_number:
                continue
            if rec.picking_type_code != 'incoming' or not rec.purchase_id:
                raise ValidationError(_(
                    "El número de pedimento solo se captura en recepciones (IN) ligadas a una "
                    "Orden de compra."))
            if not PEDIMENTO_RE.match(rec.entry_number):
                raise ValidationError(_(
                    "'%(val)s' no es un número de pedimento válido.\n\n"
                    "Formato: 15 dígitos (año 2, aduana 2, patente 4, número 7), "
                    "p. ej. 26 43 1925 6000244.\n"
                    "Si la compra no es de importación, desmarca 'Importación' en la Orden de compra.",
                    val=rec.entry_number))

    def button_validate(self):
        missing = self.filtered(lambda p: p.almx_is_import and not p.entry_number)
        if missing:
            raise UserError(_(
                "Captura el número de pedimento antes de validar: %(names)s.\n\n"
                "Es una recepción de una compra de importación.",
                names=', '.join(missing.mapped('name'))))
        return super().button_validate()
