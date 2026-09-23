import api from "../api/axios";

export interface DivulgationGroup {
    id: number;
    name: string;
    platform: string;
    category: string;
    description: string | null;
    link: string | null;
    best_time: string | null;
    member_count: number;
    status: string;
}

export interface DivulgationGroupRequest {
    name: string;
    platform: string;
    category?: string;
    description?: string;
    link?: string;
    best_time?: string;
    member_count?: number;
}

export interface GeneratedContent {
    title: string;
    caption: string;
    hashtags: string;
    target_audience: string;
    channel: string;
    estimated_commission: number;
    tone: string;
    link: string;
}

export async function listDivulgationGroups(): Promise<DivulgationGroup[]> {
    const response = await api.get("/divulgation-groups");
    return response.data.data;
}

export async function createDivulgationGroup(payload: DivulgationGroupRequest): Promise<{ id: number }> {
    const response = await api.post("/divulgation-groups", payload);
    return response.data.data;
}

export async function updateDivulgationGroup(id: number, payload: Partial<DivulgationGroupRequest>): Promise<DivulgationGroup> {
    const response = await api.put(`/divulgation-groups/${id}`, payload);
    return response.data.data;
}

export async function deleteDivulgationGroup(id: number): Promise<void> {
    await api.delete(`/divulgation-groups/${id}`);
}

export async function generateDivulgationText(productId: number, tone: string): Promise<GeneratedContent> {
    const response = await api.post("/divulgation-groups/generate-text", {
        product_id: productId,
        tone,
    });
    return response.data.data;
}
