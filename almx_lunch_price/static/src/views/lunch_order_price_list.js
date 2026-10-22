import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

export class LunchOrderPriceListController extends ListController {
    /**
     * Tras guardar la fila editada se recarga la lista para que los totales
     * (por proveedor y total general) reflejen el nuevo precio.
     *
     * Este hook se ejecuta DENTRO del mutex del guardado; si se hiciera
     * `await root.load()` aquí, la recarga esperaría al mismo mutex y la
     * pantalla se congelaría. Por eso se agenda para después de que termine.
     */
    onRecordSaved(record) {
        const result = super.onRecordSaved(record);
        setTimeout(() => this.model.root.load(), 0);
        return result;
    }
}

registry.category("views").add("almx_lunch_price_list", {
    ...listView,
    Controller: LunchOrderPriceListController,
});
