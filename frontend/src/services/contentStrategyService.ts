import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface ContentStrategyItem {
    id: number;
    product_id: number | null;
    content_type: string;
    platform: string;
    title: string;
    script: string;
    hashtags: string;
    cta: string;
    best_time: string;
    status: string;
    performance_score: number;
    created_at: string | null;
}

export async function generateStrategies(productId: number, platforms: string[]) {
    return postData<ContentStrategyItem[], { product_id: number; platforms: string[] }>(
        "/content-strategy/generate",
        { product_id: productId, platforms },
    );
}

export async function listStrategies(platform?: string, status?: string): Promise<ContentStrategyItem[]> {
    const params = new URLSearchParams();
    if (platform) params.set("platform", platform);
    if (status) params.set("status", status);
    const qs = params.toString() ? `?${params.toString()}` : "";
    return getData<ContentStrategyItem[]>(`/content-strategy${qs}`);
}

export async function updateStrategyStatus(id: number, status: string) {
    const response = await api.patch(`/content-strategy/${id}`, { status });
    return response.data.data;
}

export async function deleteStrategy(id: number) {
    return deleteData(`/content-strategy/${id}`);
}

export async function getPlatforms() {
    return getData<{ platforms: string[]; content_types: string[] }>("/content-strategy/platforms");
}
