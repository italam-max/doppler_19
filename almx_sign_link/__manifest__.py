{
    'name': 'Alamex - Botón de firmar en enlaces',
    'summary': 'Muestra Firmar ahora según las firmas pendientes del usuario, no según el enlace',
    'description': """
La pantalla de un documento de Firma decide si muestra "Firmar ahora" con el dato
need_to_sign que viene en el enlace. Si el enlace se copió de la sesión de alguien
sin firma pendiente, quien lo recibe no ve el botón aunque le falte firmar.

Este módulo consulta las firmas pendientes del usuario al abrir el documento.
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Sales/Sign',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['sign'],
    'assets': {
        'web.assets_backend': [
            'almx_sign_link/static/src/sign_request_action_patch.js',
        ],
    },
    'installable': True,
    'application': False,
}
