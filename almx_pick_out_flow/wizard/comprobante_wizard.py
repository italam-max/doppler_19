import base64

from odoo import _, api, fields, models
from odoo.exceptions import UserError

ALMX_COMPROBANTE_SIGNATURES = (b'%PDF', b'\xff\xd8\xff', b'\x89PNG')  # PDF, JPG, PNG


class AlmxComprobanteWizard(models.TransientModel):
    _name = 'almx.comprobante.wizard'
    _description = 'Comprobante de entrega'

    picking_id = fields.Many2one('stock.picking', required=True, readonly=True)
    comprobante = fields.Binary(string='Comprobante (hoja firmada)', required=True)
    comprobante_filename = fields.Char(string='Nombre del archivo')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        picking_id = self.env.context.get('almx_comprobante_picking_id')
        if picking_id and 'picking_id' in fields_list:
            res['picking_id'] = picking_id
        return res

    def action_confirm(self):
        self.ensure_one()
        raw = base64.b64decode(self.comprobante or b'')
        if not raw.startswith(ALMX_COMPROBANTE_SIGNATURES):
            raise UserError(_('El Comprobante debe ser PDF o foto (JPG/PNG) de la hoja de entrega firmada.'))
        self.picking_id.write({
            'x_studio_comprobante': self.comprobante,
            'x_studio_comprobante_filename': self.comprobante_filename or _('comprobante_%s', self.picking_id.name),
        })
        ctx = {k: v for k, v in self.env.context.items()
               if not k.startswith('default_') and k != 'almx_comprobante_picking_id'}
        pickings = self.env['stock.picking'].browse(ctx.get('button_validate_picking_ids') or self.picking_id.ids)
        return pickings.with_context(ctx).button_validate()
