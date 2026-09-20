import { getData, postData } from "./apiResponse";

export interface WhatsAppSessionStatus {
    status: string;
    phone_number: string;
    last_error: string;
    waha_reachable: boolean;
}

export interface WhatsAppMessageItem {
    id: number;
    contact_phone: string;
    contact_name: string;
    direction: "in" | "out";
    body: string;
    is_from_agent: boolean;
    created_at: string | null;
}

export interface WhatsAppConversation {
    contact_phone: string;
    contact_name: string;
    last_message: string;
    last_at: string | null;
}

export async function startSession() {
    return postData<{}, {}>("/whatsapp/session/start", {});
}

export async function getQrCode() {
    return getData<{ qr_code_base64: string }>("/whatsapp/session/qr");
}

export async function getSessionStatus() {
    return getData<WhatsAppSessionStatus>("/whatsapp/session/status");
}

export async function stopSession() {
    return postData<{}, {}>("/whatsapp/session/stop", {});
}

export async function listConversations() {
    return getData<WhatsAppConversation[]>("/whatsapp/conversations");
}

export async function listMessages(phone?: string) {
    const url = phone ? `/whatsapp/messages?phone=${encodeURIComponent(phone)}` : "/whatsapp/messages";
    return getData<WhatsAppMessageItem[]>(url);
}

export async function sendMessage(phone: string, text: string) {
    return postData<{}, { phone: string; text: string }>("/whatsapp/send", { phone, text });
}
