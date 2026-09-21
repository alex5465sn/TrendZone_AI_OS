import api from "../api/axios";

export interface FacebookPostRequest {
    message: string;
    link?: string;
    image_url?: string;
}

export async function getFacebookStatus(): Promise<{ configured: boolean; peak_hours: number[] }> {
    const response = await api.get("/facebook/status");
    return response.data.data;
}

export async function runAutoSchedule(): Promise<{ created: number }> {
    const response = await api.post("/facebook/auto-schedule/run", {});
    return response.data.data;
}

export async function postToFacebook(payload: FacebookPostRequest): Promise<any> {
    const response = await api.post("/facebook/post", payload);
    return response.data;
}

export interface GenerateVideoRequest {
    image_url: string;
    title: string;
    price: string;
    discount_rate?: number;
}

export interface GeneratedVideo {
    file: string;
    url: string;
}

export async function generateProductVideo(payload: GenerateVideoRequest): Promise<GeneratedVideo> {
    const response = await api.post("/facebook/video/generate", payload);
    return response.data.data;
}

export async function postVideoToFacebook(file: string, description: string): Promise<any> {
    const response = await api.post("/facebook/video/post", { file, description });
    return response.data;
}

export interface ScheduledPostRequest {
    product_item_id: number;
    message: string;
    link?: string;
    image_url?: string;
    video_file?: string;
    scheduled_at: string;
}

export async function createScheduledPost(payload: ScheduledPostRequest): Promise<any> {
    const response = await api.post("/scheduled-posts", payload);
    return response.data;
}

export async function listScheduledPosts(): Promise<any[]> {
    const response = await api.get("/scheduled-posts");
    return response.data.data;
}

export async function cancelScheduledPost(id: number): Promise<any> {
    const response = await api.delete(`/scheduled-posts/${id}`);
    return response.data;
}
