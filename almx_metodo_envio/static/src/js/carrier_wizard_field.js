/** @odoo-module **/
// Método de entrega en ventas de Refacciones: al elegirlo, se guarda la venta y se abre
// la ventana con los datos que pide ese método.
import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useRecordObserver } from "@web/model/relational_model/utils";
import { Many2OneField, buildM2OFieldDescription } from "@web/views/fields/many2one/many2one_field";

const KINDS_WITH_DATA = ["paqueteria", "flete", "recoleccion", "app"];
const m2oId = (v) => (v ? (Array.isArray(v) ? v[0] : v.id) : false);
const m2oName = (v) => (v ? (Array.isArray(v) ? v[1] : v.display_name) : "");

export class AlmxCarrierWizardField extends Component {
    static template = xml`<Many2OneField t-props="props"/>`;
    static components = { Many2OneField };
    static props = { ...Many2OneField.props };

    setup() {
        this.action = useService("action");
        this.lastId = undefined;
        useRecordObserver((record) => {
            const value = record.data[this.props.name];
            const id = m2oId(value);
            if (this.lastId === undefined) {
                this.lastId = id;
                return;
            }
            if (id === this.lastId) {
                return;
            }
            this.lastId = id;
            if (id && record.data.sale_type === "spare") {
                Promise.resolve().then(() => this.openWizard(record, id, m2oName(value)));
            }
        });
    }

    async openWizard(record, carrierId, carrierName) {
        const saved = await record.save();
        if (!saved || !record.resId) {
            return;
        }
        if (!KINDS_WITH_DATA.includes(record.data.almx_shipping_kind)) {
            return;
        }
        await this.action.doAction(
            {
                type: "ir.actions.act_window",
                name: carrierName,
                res_model: "almx.shipping.method.wizard",
                views: [[false, "form"]],
                target: "new",
                context: {
                    default_order_id: record.resId,
                    default_carrier_id: carrierId,
                    almx_from_select: true,
                },
            },
            { onClose: () => record.load() }
        );
    }
}

registry.category("fields").add("almx_carrier_wizard", {
    ...buildM2OFieldDescription(AlmxCarrierWizardField),
});
