from odoo import api, models

# Campos disparadores por automatización. Varios son de Studio (sin xmlid), por eso se
# asignan por nombre al instalar/actualizar el módulo.
TRIGGER_FIELDS = {"almx_automations.auto_116": [["purchase.order", "create_uid"], ["purchase.order", "state"]], "almx_automations.auto_117": [["purchase.order", "state"]], "almx_automations.auto_84": [["sale.order", "state"]], "almx_automations.auto_80": [["sale.order", "state"]], "almx_automations.auto_86": [["sale.order", "x_studio_contrato"]], "almx_automations.auto_85": [["sale.order", "x_studio_contrato"]], "almx_automations.auto_69": [["crm.lead", "type"]], "almx_automations.auto_68": [["crm.lead", "type"]], "almx_automations.auto_105": [["maintenance.request", "equipment_id"]], "almx_automations.auto_54": [["maintenance.request", "stage_id"]], "almx_automations.auto_93": [["project.task", "stage_id"]], "almx_automations.auto_94": [["project.task", "stage_id"]], "almx_automations.auto_88": [["project.task", "stage_id"]], "almx_automations.auto_90": [["project.task", "stage_id"]], "almx_automations.auto_89": [["project.task", "stage_id"]], "almx_automations.auto_137": [["helpdesk.ticket", "stage_id"]], "almx_automations.auto_104": [["helpdesk.ticket", "stage_id"]]}


class BaseAutomation(models.Model):
    _inherit = 'base.automation'

    @api.model
    def _almx_sync_trigger_fields(self):
        Fields = self.env['ir.model.fields']
        for xmlid, pairs in TRIGGER_FIELDS.items():
            automation = self.env.ref(xmlid, raise_if_not_found=False)
            if not automation:
                continue
            field_ids = [f.id for f in (Fields._get(model, name) for model, name in pairs) if f]
            automation.write({'trigger_field_ids': [(6, 0, field_ids)]})
        return True
