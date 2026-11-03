import { patch } from "@web/core/utils/patch";
import { rpc, ConnectionLostError } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { ActivityMenu } from "@hr_attendance/components/attendance_menu/attendance_menu";

patch(ActivityMenu.prototype, {
    setup() {
        super.setup();
        this.state.attendanceState = "checked_out";
    },

    _searchReadEmployeeFill() {
        super._searchReadEmployeeFill();
        if (this.employee && this.employee.id) {
            const attendanceState = this.employee.attendance_state || "checked_out";
            this.state.attendanceState = attendanceState;
            // Durante el almuerzo el empleado sigue con la asistencia abierta.
            this.state.checkedIn = attendanceState !== "checked_out";
        }
    },

    async lunchAction(action) {
        this.dropdown.close();
        try {
            this.employee = await rpc("/almx_lunch_time/systray_action", { action });
            this._searchReadEmployeeFill();
        } catch (error) {
            if (error instanceof ConnectionLostError) {
                this.notification.add(
                    _t("Connection lost. Lunch start/end could not be recorded."),
                    {
                        title: _t("Attendance Error"),
                        type: "danger",
                        sticky: false,
                    }
                );
            } else {
                throw error;
            }
        }
    },
});
