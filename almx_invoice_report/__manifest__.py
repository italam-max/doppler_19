{
    'name': 'Alamex - Formato de factura (CFDI)',
    'version': '19.0.1.0.0',
    'summary': 'Representación impresa de factura más limpia: descripción ancha, claves SAT en línea, datos fiscales en rejilla',
    'author': 'Alamex / Doppler Elevadores',
    'license': 'LGPL-3',
    'category': 'Accounting/Localizations',
    'depends': ['l10n_mx_edi', 'l10n_mx_edi_extended', 'l10n_mx_edi_landing'],
    'data': [
        'views/report_invoice.xml',
    ],
    'installable': True,
    'application': False,
}
