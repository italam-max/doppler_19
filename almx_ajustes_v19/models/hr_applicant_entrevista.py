from odoo import _, models
from odoo.exceptions import UserError


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    def action_almx_start_interview(self):
        """Entrevista presencial: el entrevistador llena el formulario del puesto.

        Reutiliza la respuesta en curso del candidato para ese formulario;
        si no hay, crea una nueva ligada al candidato (no se envía correo).
        """
        self.ensure_one()
        self.check_access("read")
        survey = self.survey_id
        if not survey:
            raise UserError(_("El puesto no tiene formulario de entrevista."))
        if not survey.active:
            raise UserError(_(
                "El formulario de entrevista \"%s\" está archivado. Actívalo antes de iniciar la entrevista.",
                survey.title,
            ))
        answer = self.sudo().response_ids.filtered(
            lambda r: r.survey_id == survey and r.state != "done"
        )[:1]
        if not answer:
            answer = survey.sudo()._create_answer(
                partner=self.partner_id,
                email=self.email_from,
                check_attempts=False,
                applicant_id=self.id,
            )
        return {
            "type": "ir.actions.act_url",
            "target": "new",
            "url": f"/survey/start/{survey.access_token}?answer_token={answer.access_token}",
        }
