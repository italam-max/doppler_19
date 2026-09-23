from . import models


def pre_init_hook(env):
    """Si el xmlid del grupo quedó en la base bajo el nombre viejo del módulo
    (strict_product_lock), se reasigna a este módulo para reutilizar el mismo
    grupo y sus miembros en lugar de crear uno nuevo."""
    env.cr.execute("""
        UPDATE ir_model_data SET module = 'almx_strict_product_lock'
         WHERE module = 'strict_product_lock' AND name = 'group_allow_product_creation'
           AND NOT EXISTS (SELECT 1 FROM ir_model_data
                            WHERE module = 'almx_strict_product_lock'
                              AND name = 'group_allow_product_creation')
    """)
