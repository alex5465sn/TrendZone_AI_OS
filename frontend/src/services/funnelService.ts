import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface FunnelCard {
    id: number;
    title: string;
    description: string;
    product_id: number | null;
    priority: string;
    position: number;
    estimated_revenue: number;
    channel: string;
    notes: string;
    created_at: string | null;
}

export interface FunnelStage {
    id: number;
    name: string;
    color: string;
    position: number;
    cards: FunnelCard[];
}

export interface CardCreate {
    stage_id: number;
    title: string;
    description?: string;
    product_id?: number | null;
    priority?: string;
    estimated_revenue?: number;
    channel?: string;
    notes?: string;
}

export async function getStages(): Promise<FunnelStage[]> {
    return getData<FunnelStage[]>("/funnel/stages");
}

export async function createCard(payload: CardCreate) {
    return postData<{ id: number; title: string }, CardCreate>("/funnel/cards", payload);
}

export async function moveCard(cardId: number, stageId: number, position: number) {
    const response = await api.put(`/funnel/cards/${cardId}/move`, { stage_id: stageId, position });
    return response.data.data;
}

export async function deleteCard(cardId: number) {
    return deleteData(`/funnel/cards/${cardId}`);
}

export async function getRadar() {
    return getData<any[]>("/funnel/radar");
}

export async function autoPopulate() {
    return postData<{ created: number }, {}>("/funnel/auto-populate", {});
}
