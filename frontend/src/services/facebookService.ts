import api from "../api/axios";

export interface FacebookPostRequest {
    message: string;
    link?: string;
    image_url?: string;
}

export async function getFacebookStatus(): Promise<{ configured: boolean }> {
    const response = await api.get("/facebook/status");
    return response.data.data;
}

export async function postToFacebook(payload: FacebookPostRequest): Promise<any> {
    const response = await api.post("/facebook/post", payload);
    return response.data;
}
