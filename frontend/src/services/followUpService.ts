import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface FollowUpItem {
    id: number;
    card_id: number | null;
    product_id: number | null;
    message: string;
    due_at: string | null;
    status: string;
    priority: string;
    created_at: string | null;
    days_overdue?: number;
}

export async function listFollowUps(status?: string): Promise<FollowUpItem[]> {
    const qs = status ? `?status=${status}` : "";
    return getData<FollowUpItem[]>(`/follow-ups${qs}`);
}

export async function getOverdueFollowUps(): Promise<FollowUpItem[]> {
    return getData<FollowUpItem[]>("/follow-ups/overdue");
}

export async function createFollowUp(payload: {
    message: string;
    card_id?: number | null;
    product_id?: number | null;
    due_at?: string;
    priority?: string;
}) {
    return postData<{ id: number }, typeof payload>("/follow-ups", payload);
}

export async function updateFollowUpStatus(id: number, status: string) {
    const response = await api.patch(`/follow-ups/${id}`, { status });
    return response.data.data;
}

export async function deleteFollowUp(id: number) {
    return deleteData(`/follow-ups/${id}`);
}
