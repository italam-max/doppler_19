import re

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.tools.misc import format_date

# Campos Studio de psicometría en hr.applicant (vienen de Odoo 16) -> campo propio del empleado
PSICO_FIELDS = {
    "x_studio_field_2kQbH": "almx_psico_test",      # Psychometric Test
    "x_studio_field_LJGRB": "almx_psico_zavic",     # Zavic
    "x_studio_field_UpoqW": "almx_psico_rain",      # Man in the Rain
    "x_studio_field_rNDk8": "almx_psico_machover",  # Machover
}
GROUP = "almx_hr_expediente.group_expediente_rh"

# Campos Studio del expediente (y su _filename) que solo lee/escribe el grupo.
# Los grupos en ir.model.fields no aplican a campos manuales en v19, por eso se usa _has_field_access.
EXPEDIENTE_FIELDS = {
    "hr.applicant": list(PSICO_FIELDS),
    "hr.employee": [
        "x_studio_field_X5eU7", "x_studio_field_7yYos", "x_studio_field_qCV3k", "x_studio_field_Lc39r",
        "x_studio_field_hLRzJ", "x_studio_id_1", "x_studio_field_4fVwu", "x_studio_drivers_license_1",
        "x_studio_military_primer_1", "x_studio_field_PxX8o", "x_studio_field_yAgYM", "x_studio_field_QxOXp",
        "x_studio_field_jH7fy", "x_studio_field_CqmyV", "x_studio_cv", "x_studio_proof_of_studies",
        "x_studio_confidenciality_agreement", "x_studio_job_description_agreement",
        "x_studio_internal_reguations_agreement", "x_studio_image_use_consent",
        "x_studio_field_gRCXE",  # contrato firmado (heredado de la versión)
    ],
    "hr.version": ["x_studio_field_gRCXE"],
}


def _almx_field_access(model, field):
    names = EXPEDIENTE_FIELDS.get(model._name, ())
    base = field.name[:-9] if field.name.endswith("_filename") else field.name
    if base not in names or model.env.su:
        return True
    return model.env.user.has_group(GROUP)


def _almx_psico_vals(applicant, employee):
    """Valores de psicometría del solicitante que el empleado aún no tiene."""
    vals = {}
    app = applicant.sudo().with_context(bin_size=False)
    emp = employee.sudo().with_context(bin_size=True)
    for src, dst in PSICO_FIELDS.items():
        if src not in app._fields or emp[dst]:
            continue
        data = app[src]
        if data:  # archivos huérfanos (sin filestore) regresan vacío y se omiten
            fname = src + "_filename"
            vals[dst] = data
            vals[dst + "_fname"] = app[fname] if fname in app._fields else False
    return vals


def seed_psico_from_applicants(env):
    """Copia la psicometría del solicitante ligado a cada empleado (instalación/actualización)."""
    employees = env["hr.employee"].sudo().with_context(active_test=False).search([])
    for emp in employees:
        app = emp._almx_find_applicant()
        vals = _almx_psico_vals(app, emp) if app else {}
        if vals:
            emp.write(vals)


# Tipo de contrato a partir del nombre que traía el contrato de Odoo 16 (orden importa)
CONTRACT_TYPE_RULES = [
    (r"j[oó]venes", "almx_hr_expediente.contract_type_jcf"),
    (r"prueba", "almx_hr_expediente.contract_type_indeterminado_prueba"),
    (r"indeterminado", "almx_hr_expediente.contract_type_indeterminado"),
    (r"determinado", "almx_hr_expediente.contract_type_determinado"),
]


def seed_contract_types(env):
    """Llena el tipo de contrato vacío de las versiones migradas usando su nombre de 16."""
    Version = env["hr.version"].sudo().with_context(active_test=False, tracking_disable=True)
    by_type = {}
    for version in Version.search([("contract_type_id", "=", False), ("name", "!=", False)]):
        name = version.name.lower()
        for pattern, xmlid in CONTRACT_TYPE_RULES:
            if re.search(pattern, name):
                by_type.setdefault(xmlid, Version)
                by_type[xmlid] |= version
                break
    for xmlid, versions in by_type.items():
        versions.write({"contract_type_id": env.ref(xmlid).id})


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    def _has_field_access(self, field, operation):
        return _almx_field_access(self, field) and super()._has_field_access(field, operation)

    @api.model_create_multi
    def create(self, vals_list):
        apps = super().create(vals_list)
        apps.filtered("employee_id")._almx_push_psico_to_employee()
        return apps

    def write(self, vals):
        res = super().write(vals)
        if "employee_id" in vals or any(f in vals for f in PSICO_FIELDS):
            self._almx_push_psico_to_employee()
        return res

    def _almx_push_psico_to_employee(self):
        """Al contratar (o subir psicometría al solicitante) se copia al empleado si está vacío."""
        for app in self.sudo():
            if app.employee_id:
                vals = _almx_psico_vals(app, app.employee_id)
                if vals:
                    app.employee_id.sudo().write(vals)


class HrVersion(models.Model):
    _inherit = "hr.version"

    def _has_field_access(self, field, operation):
        return _almx_field_access(self, field) and super()._has_field_access(field, operation)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    almx_applicant_id = fields.Many2one(
        "hr.applicant", string="Solicitud de origen",
        compute="_compute_almx_applicant_id", groups=GROUP)

    almx_psico_test = fields.Binary("Prueba psicométrica", attachment=True, groups=GROUP)
    almx_psico_test_fname = fields.Char("Archivo prueba psicométrica", groups=GROUP)
    almx_psico_zavic = fields.Binary("Zavic", attachment=True, groups=GROUP)
    almx_psico_zavic_fname = fields.Char("Archivo Zavic", groups=GROUP)
    almx_psico_rain = fields.Binary("Persona bajo la lluvia", attachment=True, groups=GROUP)
    almx_psico_rain_fname = fields.Char("Archivo Persona bajo la lluvia", groups=GROUP)
    almx_psico_machover = fields.Binary("Machover", attachment=True, groups=GROUP)
    almx_psico_machover_fname = fields.Char("Archivo Machover", groups=GROUP)

    almx_antiguedad = fields.Char("Antigüedad", compute="_compute_almx_antiguedad")
    almx_contrato_vigente = fields.Char("Contrato vigente", compute="_compute_almx_contrato_vigente", groups=GROUP)
    almx_ultimo_movimiento = fields.Char("Último movimiento", compute="_compute_almx_contrato_vigente", groups=GROUP)

    def _has_field_access(self, field, operation):
        return _almx_field_access(self, field) and super()._has_field_access(field, operation)

    def _compute_almx_antiguedad(self):
        today = fields.Date.context_today(self)
        for emp in self:
            start = emp["x_studio_fecha_de_ingreso"] if "x_studio_fecha_de_ingreso" in emp._fields else False
            end = (emp["x_studio_fecha_de_salida"] if "x_studio_fecha_de_salida" in emp._fields else False) or today
            if not start or end < start:
                emp.almx_antiguedad = False
                continue
            delta = relativedelta(end, start)
            parts = []
            if delta.years:
                parts.append(_("%s año", delta.years) if delta.years == 1 else _("%s años", delta.years))
            if delta.months:
                parts.append(_("%s mes", delta.months) if delta.months == 1 else _("%s meses", delta.months))
            if not parts:
                parts.append(_("%s día", delta.days) if delta.days == 1 else _("%s días", delta.days))
            text = ", ".join(parts)
            if emp["x_studio_fecha_de_salida"] if "x_studio_fecha_de_salida" in emp._fields else False:
                text = _("%s (hasta su salida)", text)
            emp.almx_antiguedad = text

    def _compute_almx_contrato_vigente(self):
        env = self.env
        for emp in self:
            version = emp.sudo().version_id
            if not version:
                emp.almx_contrato_vigente = emp.almx_ultimo_movimiento = False
                continue
            ctype = version.contract_type_id.name or _("Sin tipo de contrato")
            if version.contract_date_start:
                period = _("del %(start)s al %(end)s", start=format_date(env, version.contract_date_start),
                           end=format_date(env, version.contract_date_end)) if version.contract_date_end else \
                    _("desde el %s (indefinido)", format_date(env, version.contract_date_start))
                emp.almx_contrato_vigente = "%s, %s" % (ctype, period)
            else:
                emp.almx_contrato_vigente = ctype
            emp.almx_ultimo_movimiento = _("Vigente desde el %s", format_date(env, version.date_version))

    def _almx_find_applicant(self):
        """Solicitud ligada al empleado: prioriza la que tenga psicometría."""
        self.ensure_one()
        Applicant = self.env["hr.applicant"]
        src = [f for f in PSICO_FIELDS if f in Applicant._fields]
        emp = self.sudo().with_context(bin_size=True, active_test=False)
        cand = emp["x_studio_candidato"] if "x_studio_candidato" in emp._fields else Applicant
        apps = (cand | emp.applicant_ids).sorted("id", reverse=True)
        with_psico = apps.filtered(lambda a: any(a[f] for f in src))
        return (with_psico or apps)[:1]

    def _compute_almx_applicant_id(self):
        for emp in self:
            emp.almx_applicant_id = emp._almx_find_applicant().id if emp.id else False

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
