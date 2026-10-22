import logging

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuración acordada en la validación por áreas (22 oct 2026)
# ---------------------------------------------------------------------------
IT = ['italam@alam.mx', 'alexis.a@alam.mx', 'celia.a@alam.mx']
CALIDAD = ['alejandra.o@alam.mx', 'david.a@alam.mx']
DIRECCION = ['hamdi@alam.mx', 'joud@alam.mx', 'lujain@alam.mx', 'yazan@alam.mx']
RH = ['berenice.s@alam.mx', 'angel.a@alam.mx']

# Soporte: ver tickets de todas las mesas
HELPDESK_ALL_TEAMS = IT + CALIDAD + DIRECCION
# Soporte: solo IT conserva el grupo Administrador (configuración de mesas)
HELPDESK_ADMINS = IT
# Tiempo personal: pueden usar todos los tipos
LEAVE_ALL_TYPES = RH + IT + DIRECCION

# Tipos de tiempo personal que cualquier empleado puede solicitar (ids de 16/19):
# 65 Trabajo fuera de Oficina, 70 Falta justificada con goce. (la de más uso),
# 56 Falta justificada sin goce, 59 Vacaciones.
LEAVE_TYPES_FOR_EVERYONE = [65, 70, 56, 59]

# Copia de 2022 del formulario de postulación: estructura vieja que rompe el
# script de formularios de 19. Al archivarla se usa el formulario estándar.
WEBSITE_VIEWS_TO_ARCHIVE = ['website_hr_recruitment.apply']


def _users(env, logins):
    users = env['res.users'].with_context(active_test=False).search([('login', 'in', logins)])
    missing = set(logins) - set(users.mapped('login'))
    if missing:
        _logger.warning('almx_ajustes_v19: usuarios no encontrados: %s', ', '.join(sorted(missing)))
    return users.filtered('active')


def _add_users(env, group_xmlid, logins):
    group = env.ref(group_xmlid)
    users = _users(env, logins)
    users.write({'group_ids': [(4, group.id)]})
    _logger.info('almx_ajustes_v19: %s → %s', group.name, ', '.join(users.mapped('name')))


def _cleanup_helpdesk_admins(env):
    manager = env.ref('helpdesk.group_helpdesk_manager')
    helpdesk_user = env.ref('helpdesk.group_helpdesk_user')
    keep = _users(env, HELPDESK_ADMINS) | env.ref('base.user_admin')
    to_downgrade = manager.user_ids.filtered(lambda u: not u.share) - keep
    # Se quita Administrador pero se conserva Usuario de Soporte para que
    # puedan seguir creando y atendiendo sus tickets.
    to_downgrade.write({'group_ids': [(3, manager.id), (4, helpdesk_user.id)]})
    _logger.info('almx_ajustes_v19: Soporte/Administrador retirado a: %s',
                 ', '.join(to_downgrade.mapped('name')) or '(nadie)')


def _leave_types(env):
    leave_types = env['hr.leave.type'].with_context(active_test=False)
    leave_types.search([]).write({'almx_restricted': True})
    allowed = leave_types.browse(LEAVE_TYPES_FOR_EVERYONE).exists()
    allowed.write({'almx_restricted': False})
    _logger.info('almx_ajustes_v19: tipos para todos: %s', ', '.join(allowed.mapped('name')))


def _website_recruitment(env):
    views = env['ir.ui.view'].with_context(active_test=False).search([
        ('key', 'in', WEBSITE_VIEWS_TO_ARCHIVE),
        ('website_id', '!=', False),
        ('active', '=', True),
    ])
    views.write({'active': False})
    _logger.info('almx_ajustes_v19: vistas del sitio archivadas: %s', views.ids)

    # Script huérfano del módulo OCA website_form_recaptcha (no instalado en 19)
    assets = env['ir.asset'].with_context(active_test=False).search([
        ('path', 'ilike', 'website_form_recaptcha'),
    ])
    assets.unlink()
    _logger.info('almx_ajustes_v19: assets huérfanos eliminados: %s', len(assets))


def post_init_hook(env):
    _add_users(env, 'almx_ajustes_v19.group_helpdesk_all_teams', HELPDESK_ALL_TEAMS)
    _add_users(env, 'almx_ajustes_v19.group_leave_all_types', LEAVE_ALL_TYPES)
    _cleanup_helpdesk_admins(env)
    _leave_types(env)
    _website_recruitment(env)
