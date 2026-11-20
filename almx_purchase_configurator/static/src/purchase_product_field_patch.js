import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { serializeDateTime } from "@web/core/l10n/dates";
import { x2ManyCommands } from "@web/core/orm_service";
import { PurchaseOrderLineProductField } from "@purchase_product_matrix/js/purchase_product_field";
import { ProductConfiguratorDialog } from "@sale/js/product_configurator_dialog/product_configurator_dialog";

const { DateTime } = luxon;

patch(PurchaseOrderLineProductField.prototype, {
    setup() {
        super.setup(...arguments);
        this.almxDialog = useService("dialog");
    },

    async _almxUseConfigurator() {
        const template = this.props.record.data.product_template_id;
        if (!template) {
            return false;
        }
        return await this.orm.call(
            "product.template",
            "almx_purchase_use_configurator",
            [[template.id]]
        );
    },

    async _onProductTemplateUpdate() {
        if (!(await this._almxUseConfigurator())) {
            return super._onProductTemplateUpdate(...arguments);
        }
        const templateId = this.props.record.data.product_template_id.id;
        const result = await this.orm.call(
            "product.template",
            "get_single_product_variant",
            [templateId]
        );
        if (result && result.product_id) {
            await this.props.record.update({
                product_id: { id: result.product_id, display_name: result.product_name },
            });
        } else {
            this._almxOpenConfigurator(false);
        }
    },

    async onEditConfiguration() {
        if (this.props.record.data.is_configurable_product && (await this._almxUseConfigurator())) {
            return this._almxOpenConfigurator(true);
        }
        return super.onEditConfiguration(...arguments);
    },

    _almxOpenConfigurator(edit) {
        const record = this.props.record;
        const order = record.model.root;
        const line = record.data;
        const ptavIds = edit
            ? [
                  ...(line.product_template_attribute_value_ids?.currentIds || []),
                  ...(line.product_no_variant_attribute_value_ids?.currentIds || []),
              ]
            : [];
        this.almxDialog.add(ProductConfiguratorDialog, {
            productTemplateId: line.product_template_id.id,
            ptavIds,
            customPtavs: [],
            quantity: line.product_qty || 1,
            productUOMId: edit && line.product_uom_id ? line.product_uom_id.id : undefined,
            companyId: order.data.company_id?.id,
            currencyId: order.data.currency_id?.id,
            soDate: serializeDateTime(order.data.date_order || DateTime.now()),
            edit,
            options: { showPrice: false, showPackaging: false },
            save: async (mainProduct) => {
                const noVariantPtavIds = mainProduct.attribute_lines
                    .filter((ptal) => ptal.create_variant === "no_variant")
                    .flatMap((ptal) => ptal.selected_attribute_value_ids);
                const values = {
                    product_id: { id: mainProduct.id, display_name: mainProduct.display_name },
                    product_qty: mainProduct.quantity,
                    product_no_variant_attribute_value_ids: [x2ManyCommands.set(noVariantPtavIds)],
                };
                if (mainProduct.uom) {
                    values.product_uom_id = mainProduct.uom;
                }
                await record.update(values);
            },
            discard: () => {
                order.data.order_line.delete(record);
            },
        });
    },
});
