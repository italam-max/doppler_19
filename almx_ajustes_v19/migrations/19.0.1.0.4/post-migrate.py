import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

# Pueden cambiar el responsable de una aprobación
CHANGE_RESPONSIBLE = ['italam@alam.mx', 'hamdi@alam.mx']


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    group = env.ref('almx_ajustes_v19.group_approval_change_responsible')
    users = env['res.users'].search([('login', 'in', CHANGE_RESPONSIBLE)])
    users.write({'group_ids': [(4, group.id)]})
    _logger.info('almx_ajustes_v19: %s → %s', group.name, ', '.join(users.mapped('name')))
