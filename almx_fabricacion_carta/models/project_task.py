import base64
import logging

from markupsafe import Markup

from odoo import _, fields, models

_logger = logging.getLogger(__name__)

# code -> (campo generada, campo fecha, xmlid del reporte, prefijo del archivo, nombre del documento)
CARTAS = {
    'fabricacion': ('almx_carta_fab_generada', 'almx_carta_fab_fecha',
                    'almx_fabricacion_carta.action_report_carta_fabricacion',
                    'MEX-OPE-ANX-07_Carta_Fabricacion',
                    'Carta de Confirmación de Fabricación (MEX-OPE-ANX-07)'),
    'termino_fabricacion': ('almx_carta_termino_generada', 'almx_carta_termino_fecha',
                            'almx_fabricacion_carta.action_report_carta_termino_fabricacion',
                            'MEX-OPE-ANX-08_Carta_Termino_Fabricacion',
                            'Carta de Confirmación de Término de Fabricación (MEX-OPE-ANX-08)'),
    'llegada_almacen': ('almx_carta_almacen_generada', 'almx_carta_almacen_fecha',
                        'almx_fabricacion_carta.action_report_carta_llegada_almacen',
                        'MEX-OPE-ANX-09_Carta_Llegada_Almacen',
                        'Carta de Notificación de Llegada de Equipo a Almacén (MEX-OPE-ANX-09)'),
}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Nombres técnicos conservados desde 16 para que el upgrade preserve los datos.
    almx_carta_fab_generada = fields.Boolean(string='Carta de Fabricación generada', copy=False, readonly=True)
    almx_carta_fab_fecha = fields.Date(string='Emisión Carta de Fabricación', copy=False, readonly=True)
    almx_carta_termino_generada = fields.Boolean(string='Carta de Término de Fabricación generada', copy=False, readonly=True)
    almx_carta_termino_fecha = fields.Date(string='Emisión Carta de Término de Fabricación', copy=False, readonly=True)
    almx_carta_almacen_generada = fields.Boolean(string='Carta de Llegada a Almacén generada', copy=False, readonly=True)
    almx_carta_almacen_fecha = fields.Date(string='Emisión Carta de Llegada a Almacén', copy=False, readonly=True)

    def write(self, vals):
        # En 16 un JS interceptaba el statusbar y leía el id de la URL (#id=), que en 19 ya no
        # existe (/odoo/project/8/tasks/123): la carta nunca se habría generado. Ahora todo es
        # del lado del servidor y funciona desde el formulario, el kanban o por importación.
        previous = {t.id: t.stage_id for t in self} if 'stage_id' in vals else {}
        result = super().write(vals)
        if previous:
            for task in self:
                stage = task.stage_id
                code = stage.almx_carta_code
                if (code and previous[task.id] != stage
                        and previous[task.id] in stage.almx_carta_origin_stage_ids
                        and not task[CARTAS[code][0]]):
                    task._almx_generar_carta(code, previous[task.id])
        return result

    def _almx_generar_carta(self, code, origin_stage):
        self.ensure_one()
        generada_field, fecha_field, report_xmlid, prefix, doc_nombre = CARTAS[code]
        fecha = fields.Date.context_today(self)
        # Primero la fecha, para que el reporte la imprima.
        super(ProjectTask, self).write({generada_field: True, fecha_field: fecha})
        pdf, _content_type = self.env['ir.actions.report'].sudo()._render_qweb_pdf(report_xmlid, res_ids=self.ids)
        attachment = self.env['ir.attachment'].create({
            'name': '%s_%s.pdf' % (prefix, fecha.strftime('%Y%m%d')),
            'datas': base64.b64encode(pdf),
            'res_model': 'project.task',
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })
        supervisor = ', '.join(self.user_ids.mapped('name')) or _('Sin asignar')
        body = Markup(_(
            '<p><strong>%(doc)s generada</strong></p>'
            '<p>Documento emitido el <strong>%(fecha)s</strong>. Etapa: %(origen)s → %(destino)s.</p>'
            '<p>Supervisor de Operaciones: <strong>%(supervisor)s</strong></p>'
            '<p><em>Este documento no se vuelve a generar automáticamente; para otra copia usa Imprimir.</em></p>'
        )) % {
            'doc': doc_nombre, 'fecha': fecha.strftime('%d/%m/%Y'),
            'origen': origin_stage.name, 'destino': self.stage_id.name, 'supervisor': supervisor,
        }
        self.message_post(body=body, attachment_ids=attachment.ids)
        _logger.info('almx_fabricacion_carta: "%s" generada para tarea id=%s', code, self.id)
