{
    'name': 'Alamex - Candado de timbrado CFDI',
    'version': '19.0.1.0.0',
    'summary': 'Solo Finanzas puede enviar/timbrar facturas sin Folio Fiscal',
    'description': """
Las facturas de cliente mexicanas registradas y sin Folio Fiscal (UUID) solo
pueden enviarse (y por lo tanto timbrarse ante el SAT) por el grupo
"Puede timbrar CFDI (Finanzas)". Una vez timbradas, cualquier usuario con
acceso puede reenviarlas.
    """,
    'author': 'Alamex / Doppler Elevadores',
    'license': 'LGPL-3',
    'category': 'Accounting/Localizations',
    'depends': ['account', 'l10n_mx_edi'],
    'data': [
        'security/security.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
}
