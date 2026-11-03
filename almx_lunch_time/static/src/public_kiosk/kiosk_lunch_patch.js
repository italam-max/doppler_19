import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { deserializeDateTime } from "@web/core/l10n/dates";
import kioskApp from "@hr_attendance/public_kiosk/public_kiosk_app";
import { KioskGreetings } from "@hr_attendance/components/greetings/greetings";
import { KioskPinCode } from "@hr_attendance/components/pin_code/pin_code";
import { KioskLunchActions } from "@almx_lunch_time/public_kiosk/kiosk_lunch_actions";

const KioskAttendanceApp = kioskApp.kioskAttendanceApp;

patch(KioskAttendanceApp, {
    components: { ...KioskAttendanceApp.components, KioskLunchActions },
});

patch(KioskAttendanceApp.prototype, {
    setup() {
        super.setup();
        this.pendingAction = null;
        this.pendingBarcode = null;
    },

    switchDisplay(screen) {
        if (screen === "lunch") {
            this.state.active_display = "lunch";
            return;
        }
        return super.switchDisplay(screen);
    },

    kioskReturn(...args) {
        this.pendingAction = null;
        this.pendingBarcode = null;
        return super.kioskReturn(...args);
    },

    /** Selección manual: si ya está dentro, se ofrecen las acciones de almuerzo. */
    async kioskConfirm(employeeId) {
        this.pendingAction = null;
        this.pendingBarcode = null;
        const employee = await rpc("/hr_attendance/attendance_employee_data", {
            token: this.props.token,
            employee_id: employeeId,
        });
        if (employee && employee.employee_name && employee.attendance_state &&
            employee.attendance_state !== "checked_out") {
            this.employeeData = employee;
            this.switchDisplay("lunch");
            return;
        }
        return super.kioskConfirm(employeeId);
    },

    /** Gafete: si ya está dentro, se ofrecen las acciones de almuerzo. */
    async onBarcodeScanned(barcode) {
        if (this.lockScanner || this.state.active_display !== "main") {
            return;
        }
        this.lockScanner = true;
        let employee = {};
        try {
            employee = await rpc("/almx_lunch_time/employee_by_barcode", {
                token: this.props.token,
                barcode,
            });
        } catch {
            employee = {};
        } finally {
            this.lockScanner = false;
        }
        if (employee && employee.employee_name && employee.attendance_state &&
            employee.attendance_state !== "checked_out") {
            this.employeeData = employee;
            this.pendingBarcode = barcode;
            this.pendingAction = null;
            this.switchDisplay("lunch");
            return;
        }
        return super.onBarcodeScanned(barcode);
    },

    /** El empleado eligió una acción en la pantalla de almuerzo. */
    async onLunchAction(action) {
        this.pendingAction = action;
        if (this.pendingBarcode) {
            // El gafete ya identifica al empleado.
            return this.performLunchAction(action, { barcode: this.pendingBarcode });
        }
        if (this.employeeData.use_pin) {
            this.employeeData = { ...this.employeeData, pending_action: action };
            this.switchDisplay("pin");
            return;
        }
        return this.performLunchAction(action, { employeeId: this.employeeData.id });
    },

    /** La pantalla de PIN confirma con ``onManualSelection``. */
    async onManualSelection(employeeId, enteredPin) {
        if (this.pendingAction) {
            return this.performLunchAction(this.pendingAction, {
                employeeId,
                pin: enteredPin,
            });
        }
        return super.onManualSelection(employeeId, enteredPin);
    },

    async performLunchAction(action, { employeeId = false, pin = false, barcode = false } = {}) {
        const params = {
            token: this.props.token,
            action,
            employee_id: employeeId,
            pin_code: pin,
            barcode,
        };
        let result;
        try {
            // La geolocalización solo se registra en la salida.
            result =
                action === "check_out"
                    ? await this.makeRpcWithGeolocation("/almx_lunch_time/kiosk_action", params)
                    : await rpc("/almx_lunch_time/kiosk_action", params);
        } catch (error) {
            this.displayNotification(
                (error.data && error.data.message) || _t("The action could not be recorded.")
            );
            this.kioskReturn();
            return;
        }
        if (result && result.attendance) {
            this.pendingAction = null;
            this.pendingBarcode = null;
            this.employeeData = result;
            this.switchDisplay("greet");
        } else if (pin) {
            this.displayNotification(_t("Wrong Pin"));
        }
    },
});

patch(KioskGreetings.prototype, {
    setup() {
        super.setup();
        const data = this.props.employeeData;
        this.lunchAction = data.lunch_action || false;
        this.lunchTime = data.lunch_time
            ? this.formatDateTime(deserializeDateTime(data.lunch_time))
            : "";
    },
});

patch(KioskPinCode.prototype, {
    setup() {
        super.setup();
        const labels = {
            lunch_start: _t("start your lunch"),
            lunch_end: _t("end your lunch"),
            check_out: _t("check out"),
        };
        this.actionLabel =
            labels[this.props.employeeData.pending_action] ||
            (this.checkedIn ? _t("check out") : _t("check in"));
    },
});
