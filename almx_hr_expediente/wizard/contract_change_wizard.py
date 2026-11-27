from markupsafe import Markup

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_amount, format_date

MOVEMENTS = [
    ("nuevo", "Contrato nuevo / reingreso"),
    ("renovacion", "Renovación de contrato"),
    ("aumento", "Aumento o modificación salarial"),
    ("cambio", "Cambio de puesto o condiciones"),
]


class AlmxContractChangeWizard(models.TransientModel):
    _name = "almx.contract.change.wizard"
    _description = "Registrar movimiento de contrato"

    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True, readonly=True)
    company_id = fields.Many2one(related="employee_id.company_id")
    currency_id = fields.Many2one(related="employee_id.company_id.currency_id")

    # Contrato vigente (solo lectura, para comparar)
    current_date_version = fields.Date("Vigente desde", compute="_compute_current")
    current_contract_type_id = fields.Many2one("hr.contract.type", "Tipo de contrato", compute="_compute_current")
    current_job_id = fields.Many2one("hr.job", "Puesto", compute="_compute_current")
    current_wage = fields.Monetary("Salario mensual", currency_field="currency_id", compute="_compute_current")
    current_period = fields.Char("Periodo del contrato", compute="_compute_current")

    # Nuevo movimiento
    movement_type = fields.Selection(MOVEMENTS, string="Tipo de movimiento", required=True, default="aumento")
    date_version = fields.Date("Entra en vigor el", required=True, default=fields.Date.context_today)
    contract_type_id = fields.Many2one("hr.contract.type", "Tipo de contrato")
    contract_date_start = fields.Date("Inicio del contrato")
    contract_date_end = fields.Date("Fin del contrato", help="Solo para contratos por tiempo determinado o con periodo de prueba.")
    job_id = fields.Many2one("hr.job", "Puesto")
    wage = fields.Monetary("Salario mensual", currency_field="currency_id")
    signed_contract = fields.Binary("Contrato firmado")
    signed_contract_fname = fields.Char()
    note = fields.Text("Observaciones")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        emp = self.env["hr.employee"].browse(res.get("employee_id"))
        version = emp.sudo().version_id if emp else False
        if version:
            res.update({
                "contract_type_id": version.contract_type_id.id,
                "contract_date_start": fields.Date.to_string(version.contract_date_start),
                "contract_date_end": fields.Date.to_string(version.contract_date_end),
                "job_id": version.job_id.id,
                "wage": version.wage,
            })
        return res

    @api.depends("employee_id")
    def _compute_current(self):
        for wiz in self:
            version = wiz.employee_id.sudo().version_id
            wiz.current_date_version = version.date_version
            wiz.current_contract_type_id = version.contract_type_id
            wiz.current_job_id = version.job_id
            wiz.current_wage = version.wage
            start = format_date(self.env, version.contract_date_start) if version.contract_date_start else ""
            end = format_date(self.env, version.contract_date_end) if version.contract_date_end else _("indefinido")
            wiz.current_period = _("%(start)s al %(end)s", start=start, end=end) if start else _("Sin fechas de contrato")

    @api.onchange("movement_type", "date_version")
    def _onchange_movement_type(self):
        if self.movement_type in ("nuevo", "renovacion"):
            self.contract_date_start = self.date_version
            if self.movement_type == "nuevo":
                self.contract_date_end = False

    def action_confirm(self):
        self.ensure_one()
        emp = self.employee_id
        Version = self.env["hr.version"].sudo().with_context(active_test=False)
        if Version.search_count([("employee_id", "=", emp.id), ("date_version", "=", self.date_version)]):
            raise UserError(_(
                "Ya hay un movimiento de contrato de %(emp)s con fecha %(date)s. "
                "Corrígelo desde el Historial de contratos o usa otra fecha.",
                emp=emp.name, date=format_date(self.env, self.date_version)))
        if self.movement_type in ("nuevo", "renovacion") and not self.contract_date_start:
            raise UserError(_("Indica la fecha de inicio del contrato."))
        if self.contract_date_start and self.contract_date_end and self.contract_date_end < self.contract_date_start:
            raise UserError(_("La fecha de fin del contrato no puede ser anterior a la de inicio."))

        previous = emp.sudo()._get_version(self.date_version) or Version
        label = dict(MOVEMENTS)[self.movement_type]
        vals = {
            "date_version": self.date_version,
            "name": "%s/%s" % (emp.name, self.contract_type_id.name or label),
            "contract_type_id": self.contract_type_id.id,
            "contract_date_start": self.contract_date_start,
            "contract_date_end": self.contract_date_end,
            "job_id": self.job_id.id,
            "wage": self.wage,
            # nunca heredar el PDF del contrato anterior
            "x_studio_field_gRCXE": self.signed_contract or False,
            "x_studio_field_gRCXE_filename": self.signed_contract_fname if self.signed_contract else False,
        }
        version = emp.create_version(vals)
        emp._almx_log_contract_movement(label, self, previous, version)
        return {"type": "ir.actions.client", "tag": "soft_reload"}


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def action_almx_contract_change(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Registrar movimiento de contrato"),
            "res_model": "almx.contract.change.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_employee_id": self.id},
        }

    def _almx_log_contract_movement(self, label, wiz, previous, version):
        env = self.env
        currency = wiz.currency_id

        def d(value):
            return format_date(env, value) if value else "—"

        changes = [
            (_("Tipo de contrato"), previous.contract_type_id.name or "—", version.contract_type_id.name or "—"),
            (_("Puesto"), previous.job_id.name or "—", version.job_id.name or "—"),
            (_("Inicio del contrato"), d(previous.contract_date_start), d(version.contract_date_start)),
            (_("Fin del contrato"), d(previous.contract_date_end), d(version.contract_date_end)),
            (_("Salario mensual"), format_amount(env, previous.wage or 0.0, currency),
             format_amount(env, version.wage or 0.0, currency)),
        ]
        rows = Markup("").join(
            Markup("<li>%s: %s → <b>%s</b></li>") % (name, old, new)
            for name, old, new in changes if old != new
        ) or Markup("<li>%s</li>") % _("Sin cambios en tipo, puesto, fechas ni salario")
        signed = wiz.signed_contract_fname or _("adjunto") if wiz.signed_contract else _("pendiente de subir")
        body = Markup("<p><b>%s</b>: %s<br/>%s: %s</p><ul>%s</ul><p>%s: %s</p>") % (
            _("Movimiento de contrato"), label,
            _("Entra en vigor"), d(version.date_version),
            rows, _("Contrato firmado"), signed,
        )
        if wiz.note:
            body += Markup("<p>%s: %s</p>") % (_("Observaciones"), wiz.note)
        self.message_post(body=body, subtype_xmlid="mail.mt_note")
