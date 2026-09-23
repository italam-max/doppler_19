from . import models

# Responsables vigentes al portar (sept 2026), por login para no depender de ids.
_DEFAULT_USERS = {
    'task_sku': 'diego.u@alam.mx',
    'task_fotos': 'sabrina.f@alam.mx',
    'task_sat': 'silvia.f@alam.mx',
    'task_ficha_interna': 'zuriel.v@alam.mx',
    'task_ficha_proveedor': 'leonel.j@alam.mx',
    'task_calidad': 'alejandra.o@alam.mx',
}


def pre_init_hook(env):
    """El tipo de actividad existía bajo el nombre viejo del módulo; se reasigna
    su xmlid para reutilizarlo (conserva las actividades abiertas)."""
    env.cr.execute("""
        UPDATE ir_model_data SET module = 'almx_solicitud_actualizacion_producto'
         WHERE module = 'solicitud_actualizacion_producto'
           AND name = 'mail_activity_type_actualizacion_producto'
           AND NOT EXISTS (SELECT 1 FROM ir_model_data
                            WHERE module = 'almx_solicitud_actualizacion_producto'
                              AND name = 'mail_activity_type_actualizacion_producto')
    """)


def post_init_hook(env):
    Users = env['res.users'].with_context(active_test=False)
    for xmlid, login in _DEFAULT_USERS.items():
        task = env.ref('almx_solicitud_actualizacion_producto.%s' % xmlid, raise_if_not_found=False)
        user = Users.search([('login', '=', login)], limit=1)
        if task and user and not task.user_id:
            task.user_id = user
