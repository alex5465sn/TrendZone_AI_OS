import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface OpportunityProduct {
    id: number;
    item_id: number;
    name: string;
    image: string;
    offer_link: string;
    price: number;
    commission: number;
    rating: number;
    sales: number;
    score: number;
    confidence: number;
    recommendation: string;
}

export interface OpportunityContent {
    title: string;
    caption: string;
    hashtags: string;
    target_audience: string;
    channel: string;
    estimated_commission: number;
}

export interface Opportunity {
    product: OpportunityProduct;
    decision: string;
    content: OpportunityContent;
}

export interface Campaign {
    id: number;
    product_id: number;
    title: string;
    caption: string;
    hashtags: string;
    target_audience: string;
    channel: string;
    status: string;
    created_at: string;
}

export interface SaveCampaignPayload {
    product_id: number;
    title: string;
    caption: string;
    hashtags: string;
    target_audience: string;
    channel: string;
}

export async function getOpportunities(limit = 10): Promise<Opportunity[]> {
    return getData<Opportunity[]>(`/opportunities?limit=${limit}`);
}

export async function saveCampaign(payload: SaveCampaignPayload) {
    return postData<{ id: number; uuid: string; status: string }, SaveCampaignPayload>(
        "/opportunities/campaigns",
        payload,
    );
}

export async function listCampaigns(): Promise<Campaign[]> {
    return getData<Campaign[]>("/opportunities/campaigns");
}

export async function publishCampaign(id: number) {
    const response = await api.patch(`/opportunities/campaigns/${id}/publish`);
    return response.data.data;
}

export async function deleteCampaign(id: number) {
    return deleteData(`/opportunities/campaigns/${id}`);
}
