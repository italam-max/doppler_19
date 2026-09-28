from odoo import fields, models

# Mismos valores que la selección "Evento" (x_studio_field_9xkQk) del modelo Studio de 16.
EVENT_TYPES = [(v, v) for v in [
    'Curso de Inducción', 'Capacitación', 'Promoción', 'Carta de Agradecimiento', 'Incentivo Especial',
    'Logro de Implementación', 'Logro de Performance', 'Entrega en Tiempo y Forma', 'Entrega de Excelencia',
    'Trabajo Extra para Lograr Objetivos', 'Mejora de Procesos', 'Sugerencia Creativa',
    'Buen Trabajo en Equipo', 'Acta Administrativa', 'Sanción', 'Pérdida de Bono', 'Goals Agreement',
    'Descuento por Performance', 'Descuento por Resguardo de Materiales de Trabajo', 'Descuento por Préstamo',
    'Llamado de Atención', 'Aviso de Trabajo Extemporáneo', 'Entrega de Baja Calidad',
    'Falta de Trabajo en Equipo', 'Préstamo', 'Suspensión de Labores', 'Inscripción a Curso Externo',
    'Offboarding', 'Resguardo', 'References', 'Acta de Hechos', 'Accidente', 'Descuento',
    'Entrega de tarjeta de Vales', 'Entrega de Credencial', 'Solicitud de vacaciones',
]]


class AlmxEmployeeFile(models.Model):
    """Reemplaza el modelo Studio x_hr.employee.file de 16, que el upgrade a 19 no conservó."""
    _name = 'almx.employee.file'
    _description = 'Expediente del empleado (evento de RH)'
    _inherit = ['mail.thread']
    _order = 'date desc, id desc'
    _rec_name = 'event_type'

    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True, index=True, ondelete='cascade', tracking=True)
    event_type = fields.Selection(EVENT_TYPES, string='Evento', required=True, tracking=True)
    date = fields.Date(string='Fecha', required=True, default=fields.Date.context_today, tracking=True)
    reference_employee_id = fields.Many2one('hr.employee', string='Referencia de evento',
                                            help='Quién reporta o autoriza el evento.')
    description = fields.Text(string='Descripción')
    attachment = fields.Binary(string='Archivo adjunto', attachment=True)
    attachment_filename = fields.Char(string='Nombre del archivo')
    company_id = fields.Many2one(related='employee_id.company_id', store=True)
