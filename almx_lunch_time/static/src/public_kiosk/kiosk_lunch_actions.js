import { Component, onWillDestroy } from "@odoo/owl";

// Sin regreso automatico, el kiosko se queda en la pantalla del empleado anterior.
const LUNCH_SCREEN_TIMEOUT = 30000;

/**
 * Pantalla del kiosko que se muestra cuando el empleado ya tiene la asistencia
 * abierta: permite elegir entre iniciar/terminar el almuerzo o registrar la salida.
 */
export class KioskLunchActions extends Component {
    static template = "almx_lunch_time.KioskLunchActions";
    static props = {
        employeeData: { type: Object },
        onLunchAction: { type: Function },
        onClickBack: { type: Function },
    };

    setup() {
        const timeout = setTimeout(() => this.props.onClickBack(), LUNCH_SCREEN_TIMEOUT);
        onWillDestroy(() => clearTimeout(timeout));
    }

    get state() {
        return this.props.employeeData.attendance_state;
    }
}
