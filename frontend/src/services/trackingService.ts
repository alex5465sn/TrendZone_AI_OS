import api from "../api/axios";

export interface CreateTrackingPayload {
    product_item_id: number;
    product_name?: string;
    destination_url: string;
    channel?: string;
    post_format?: string;
    message?: string;
}

export interface TrackingLink {
    tracking_code: string;
    tracking_url: string;
}

export async function createTrackingLink(payload: CreateTrackingPayload): Promise<TrackingLink> {
    const response = await api.post("/tracking/create", payload);
    return response.data.data as TrackingLink;
}

export interface TrackingStat {
    id: number;
    tracking_code: string;
    product_item_id: number;
    product_name: string;
    destination_url: string;
    channel: string;
    post_format: string;
    click_count: number;
    created_at: string | null;
}

export async function listTrackingStats(): Promise<TrackingStat[]> {
    const response = await api.get("/tracking");
    return response.data.data as TrackingStat[];
}
