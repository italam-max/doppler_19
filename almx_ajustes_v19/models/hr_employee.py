from odoo import fields, models

# Catálogos del SAT tal como estaban en nomina_cfdi_ee (Odoo 16).
REGIMEN = [
    ('02', '02 - Sueldos'),
    ('03', '03 - Jubilados'),
    ('04', '04 - Pensionados'),
    ('05', '05 - Asimilados Miembros Sociedades Cooperativas Produccion'),
    ('06', '06 - Asimilados Integrantes Sociedades Asociaciones Civiles'),
    ('07', '07 - Asimilados Miembros consejos'),
    ('08', '08 - Asimilados comisionistas'),
    ('09', '09 - Asimilados Honorarios'),
    ('10', '10 - Asimilados acciones'),
    ('11', '11 - Asimilados otros'),
    ('12', '12 - Jubilados o Pensionados'),
    ('13', '13 - Indemnización o Separación'),
    ('99', '99 - Otro Regimen'),
]
CONTRATO = [
    ('01', '01 - Contrato de trabajo por tiempo indeterminado'),
    ('02', '02 - Contrato de trabajo para obra determinada'),
    ('03', '03 - Contrato de trabajo por tiempo determinado'),
    ('04', '04 - Contrato de trabajo por temporada'),
    ('05', '05 - Contrato de trabajo sujeto a prueba'),
    ('06', '06 - Contrato de trabajo con capacitación inicial'),
    ('07', '07 - Modalidad de contratación por pago de hora laborada'),
    ('08', '08 - Modalidad de trabajo por comisión laboral'),
    ('09', '09 - Modalidades de contratación donde no existe relación de trabajo'),
    ('10', '10 - Jubilación, pensión, retiro'),
    ('99', '99 - Otro contrato'),
]
JORNADA = [
    ('01', '01 - Diurna'),
    ('02', '02 - Nocturna'),
    ('03', '03 - Mixta'),
    ('04', '04 - Por hora'),
    ('05', '05 - Reducida'),
    ('06', '06 - Continuada'),
    ('07', '07 - Partida'),
    ('08', '08 - Por turnos'),
    ('99', '99 - Otra Jornada'),
]


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Datos SAT / IMSS de solo consulta (la nómina se lleva en NOI).
    # Se recuperan de nomina_cfdi_ee (16) con _data_recovery.
    almx_no_empleado = fields.Char('Número de empleado', readonly=True, groups='hr.group_hr_user')
    almx_rfc = fields.Char('RFC', readonly=True, groups='hr.group_hr_user')
    almx_curp = fields.Char('CURP', readonly=True, groups='hr.group_hr_user')
    almx_nss = fields.Char('Seguro social (NSS)', readonly=True, groups='hr.group_hr_user')
    almx_nombre = fields.Char('Nombre (SAT)', readonly=True, groups='hr.group_hr_user')
    almx_apellido_paterno = fields.Char('Apellido paterno', readonly=True, groups='hr.group_hr_user')
    almx_apellido_materno = fields.Char('Apellido materno', readonly=True, groups='hr.group_hr_user')
    almx_registro_patronal = fields.Char('Registro patronal', readonly=True, groups='hr.group_hr_user')
    almx_regimen = fields.Selection(REGIMEN, 'Régimen', readonly=True, groups='hr.group_hr_user')
    almx_contrato = fields.Selection(CONTRATO, 'Tipo de contrato (SAT)', readonly=True, groups='hr.group_hr_user')
    almx_jornada = fields.Selection(JORNADA, 'Jornada', readonly=True, groups='hr.group_hr_user')
    almx_sindicalizado = fields.Boolean('Sindicalizado', readonly=True, groups='hr.group_hr_user')
    almx_estado_labora_id = fields.Many2one(
        'res.country.state', 'Estado donde labora', readonly=True, groups='hr.group_hr_user')
    almx_cp_fiscal = fields.Char('Código postal (SAT)', readonly=True, groups='hr.group_hr_user')
