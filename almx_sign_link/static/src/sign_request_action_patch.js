import { onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { SignRequest } from "@sign/backend_components/sign_request/sign_request_action";

patch(SignRequest.prototype, {
    setup() {
        super.setup();
        if (this.props.action?.tag !== "sign.Document") {
            return;
        }
        onWillStart(async () => {
            const documentId = Number(this.signInfo.get("documentId"));
            if (!documentId) {
                return;
            }
            try {
                const needToSign = await this.orm.call(
                    "sign.request",
                    "almx_current_user_needs_to_sign",
                    [[documentId]]
                );
                this.signInfo.set({ needToSign });
            } catch (error) {
                // Si la consulta falla, se conserva lo que traía el enlace.
                console.warn("almx_sign_link: no se pudo consultar la firma pendiente", error);
            }
        });
    },
});
