import { Attachment } from "@mail/core/common/attachment_model";
import { Message } from "@mail/core/common/message_model";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";

const UNLOCKED_MODELS = ["discuss.channel"];

function isLocked(message) {
    if (session.almx_can_edit_chatter) {
        return false;
    }
    return !UNLOCKED_MODELS.includes(message?.thread?.model);
}

// Oculta "Editar" y "Eliminar" en los mensajes del chatter.
patch(Message.prototype, {
    get editable() {
        if (isLocked(this)) {
            return false;
        }
        return super.editable;
    },
});

// Oculta la "x" para quitar adjuntos de un mensaje ya publicado.
patch(Attachment.prototype, {
    get isDeletable() {
        if (this.message && isLocked(this.message)) {
            return false;
        }
        return super.isDeletable;
    },
});
