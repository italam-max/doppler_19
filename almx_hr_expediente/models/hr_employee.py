from odoo import _, fields, models

# Campos Studio de psicometría en hr.applicant (vienen de Odoo 16) -> campo calculado en el empleado
PSICO_FIELDS = {
    "x_studio_field_2kQbH": "almx_psico_test",      # Psychometric Test
    "x_studio_field_LJGRB": "almx_psico_zavic",     # Zavic
    "x_studio_field_UpoqW": "almx_psico_rain",      # Man in the Rain
    "x_studio_field_rNDk8": "almx_psico_machover",  # Machover
}
GROUP = "almx_hr_expediente.group_expediente_rh"


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    almx_applicant_id = fields.Many2one(
        "hr.applicant", string="Solicitud de reclutamiento",
        compute="_compute_almx_applicant_id", groups=GROUP)

    almx_psico_test = fields.Binary("Prueba psicométrica", compute="_compute_almx_psico", groups=GROUP)
    almx_psico_test_fname = fields.Char(compute="_compute_almx_psico", groups=GROUP)
    almx_psico_zavic = fields.Binary("Zavic", compute="_compute_almx_psico", groups=GROUP)
    almx_psico_zavic_fname = fields.Char(compute="_compute_almx_psico", groups=GROUP)
    almx_psico_rain = fields.Binary("Persona bajo la lluvia", compute="_compute_almx_psico", groups=GROUP)
    almx_psico_rain_fname = fields.Char(compute="_compute_almx_psico", groups=GROUP)
    almx_psico_machover = fields.Binary("Machover", compute="_compute_almx_psico", groups=GROUP)
    almx_psico_machover_fname = fields.Char(compute="_compute_almx_psico", groups=GROUP)

    def _compute_almx_applicant_id(self):
        Applicant = self.env["hr.applicant"]
        src = [f for f in PSICO_FIELDS if f in Applicant._fields]
        for emp in self:
            emp_su = emp.sudo().with_context(bin_size=True, active_test=False)
            cand = emp_su["x_studio_candidato"] if "x_studio_candidato" in emp._fields else Applicant
            apps = (cand | emp_su.applicant_ids).sorted("id", reverse=True)
            with_psico = apps.filtered(lambda a: any(a[f] for f in src))
            emp.almx_applicant_id = (with_psico or apps)[:1].id

    def _compute_almx_psico(self):
        Applicant = self.env["hr.applicant"]
        for emp in self:
            app = emp.almx_applicant_id.sudo()
            for src, dst in PSICO_FIELDS.items():
                ok = bool(app) and src in Applicant._fields
                fname = src + "_filename"
                emp[dst] = app[src] if ok else False
                emp[dst + "_fname"] = app[fname] if ok and fname in Applicant._fields else False

    def action_almx_contract_history(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Historial de contratos - %s", self.name),
            "res_model": "hr.version",
            "view_mode": "list",
            "views": [(self.env.ref("almx_hr_expediente.hr_version_list_almx_expediente").id, "list")],
            "domain": [("employee_id", "=", self.id)],
            "context": {"active_test": False, "create": False},
            "target": "current",
        }
