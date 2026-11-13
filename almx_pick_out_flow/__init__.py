from . import models
from . import wizard


def almx_set_comprobante_types(env):
    """Comprobante obligatorio en el OUT de los almacenes que trabajan PICK → OUT (WHTL)."""
    warehouses = env['stock.warehouse'].search([('delivery_steps', 'in', ('pick_ship', 'pick_pack_ship'))])
    warehouses.out_type_id.write({'almx_require_comprobante': True})


def post_init_hook(env):
    almx_set_comprobante_types(env)
