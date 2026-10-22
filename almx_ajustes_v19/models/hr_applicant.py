from datetime import datetime

import pytz

from odoo import models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    def format_date_to_tz(self):
        """Fecha de ingreso propuesta para la plantilla "Applicant: Job Offer
        (AADM-MX-RH-FO-009)". En 16 la daba almx_hr_recruitment (Portcities).

        Se conserva el mismo formato de 16 (fecha + hora). Para mostrar solo la
        fecha, cambiar el formato a '%d/%m/%Y'.
        """
        self.ensure_one()
        if not self.availability:
            return ''
        tz_name = self.env.user.tz or self.user_id.tz or 'America/Mexico_City'
        now_local = datetime.now(pytz.timezone(tz_name))
        return datetime.combine(self.availability, now_local.time()).strftime('%d/%m/%Y %H:%M:%S')
