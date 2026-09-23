from . import models


def post_init_hook(env):
    """Marca como proveedor de importación a los proveedores (empresa) cuyo
    país está capturado y es distinto al de la compañía."""
    env.cr.execute("""
        UPDATE res_partner p SET almx_import_vendor = TRUE
          FROM res_country c
         WHERE p.country_id = c.id AND c.code <> 'MX'
           AND p.is_company AND p.supplier_rank > 0
    """)
