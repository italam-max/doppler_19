import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class KioskAppAction extends Component {
    static template = "almx_lunch_time.KioskAppAction";
    static props = ["*"];
}

registry.category("actions").add("almx_lunch_time.kiosk_app", KioskAppAction);
