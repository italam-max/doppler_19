# -*- coding: utf-8 -*-
{
    'name': 'ALMX Configurador de producto en Compras',
    'version': '19.0.1.3.0',
    'summary': 'En la PO, los productos con demasiadas combinaciones se configuran con el configurador de producto en lugar de la matriz.',
    'description': """
ALMX Configurador de producto en Compras
==========================================

Problema: en Compras, Odoo 19 configura los productos con atributos mediante
la matriz (purchase_product_matrix), que arma TODAS las combinaciones. Con
productos como "Elevador MRL-G" (41 atributos) el proceso se queda sin
memoria, Odoo.sh lo mata y la línea queda sin variante ni unidad
("la unidad no tiene registros").

Qué hace:
- Si la plantilla tiene más combinaciones que el límite
  (parámetro almx_purchase_configurator.matrix_limit, por defecto 200),
  la línea de compra abre el configurador de producto (el mismo de Ventas)
  para elegir la combinación que realmente se pide al proveedor. Si la
  variante no existe, Odoo la crea al confirmar.
- Los productos con pocas combinaciones siguen usando la matriz.
- Candado en servidor: la matriz ya no se arma para esas plantillas
  (aviso en lugar de matar el proceso).
- El PDF de la PO omite la cuadrícula de esas plantillas (las líneas sí salen).
- Botón "Copiar equipo de la venta" en la solicitud de cotización: con el
  número de SO (se toma de la referencia de proveedor u origen) trae las
  variantes, cantidades, atributos sin variante y valores personalizados tal
  como los configuró Ventas. Se lee la venta con sudo porque la mayoría de
  Compras no tiene acceso a Ventas. Después se puede ajustar cada línea con
  el configurador si al proveedor se le pide distinto.
- Crear la PO desde la venta: botón "Crear solicitud de compra" en la SO
  (solo grupo de Compras) y menú Compras > Pedidos > "Crear PO desde venta"
  para quien no tiene acceso a Ventas. Pide proveedor, copia el equipo y
  abre la nueva solicitud de compra.
- Solo ventas de Equipo Nuevo (sale_type = project): el botón no aparece
  en otras ventas y el asistente rechaza SO de otro tipo.
- Botones y menú solo para el grupo "Compras: crear PO desde venta"
  (Leonel, Martha, Angélica, IT y Hamdi); el grupo general de Compras
  (p. ej. David y Saúl, que solo validan un campo) no los ve.

Changelog
----------
- 19.0.1.3.0: Solo ventas de Equipo Nuevo.
- 19.0.1.2.0: Crear PO desde la venta (botón en SO y menú en Compras).
- 19.0.1.1.0: Botón "Copiar equipo de la venta".
- 19.0.1.0.0: Versión inicial.
""",
    'author': 'Irving Sammer González Correa',
    'category': 'Inventory/Purchase',
    'depends': ['purchase_product_matrix', 'sale', 'almx_sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_config_parameter.xml',
        'views/purchase_sale_copy_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'almx_purchase_configurator/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
