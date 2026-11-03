import { Component } from "@odoo/owl";

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

    get state() {
        return this.props.employeeData.attendance_state;
    }
}
