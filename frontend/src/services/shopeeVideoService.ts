import api from "../api/axios";

export interface GenerateShopeeVideoRequest {
    image_url: string;
    title: string;
    price: string;
    discount_rate?: number;
    commission_rate?: number;
    item_id?: number;
}

export interface GeneratedShopeeVideo {
    file: string;
    url: string;
    caption: string;
}

export async function generateShopeeVideo(payload: GenerateShopeeVideoRequest): Promise<GeneratedShopeeVideo> {
    const response = await api.post("/shopee-video/generate", payload);
    return response.data.data;
}
