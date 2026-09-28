{
    'name': 'Alamex - Incapacidad Días Naturales',
    'version': '19.0.1.2.0',
    'summary': 'Las ausencias de tipo incapacidad cuentan días naturales',
    'description': """
Los tipos de ausencia marcados con "Contar días naturales (Incapacidad)" calculan
la duración en días naturales (incluye sábados, domingos y festivos), como las
incapacidades del IMSS. Vacaciones y demás tipos conservan el cálculo nativo.
""",
    'author': 'Alamex / Doppler Elevadores',
    'website': 'https://www.alam.mx',
    'category': 'Human Resources/Time Off',
    'depends': ['hr_holidays'],
    'data': [
        'views/hr_leave_type_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
