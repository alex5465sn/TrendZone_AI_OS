import { getData, postData } from "./apiResponse";
import api from "../api/axios";

export interface SaleItem {
    id: number;
    conversion_id: string;
    order_id: string;
    order_status: string;
    buyer_type: string;
    device: string;
    product_type: string;
    click_time: string;
    purchase_time: string;
    total_commission: number;
    net_commission: number;
    seller_commission: number;
    shopee_commission: number;
    utm_content: string;
    status: string;
    created_at: string;
}

export interface FinancialSummary {
    total_sales: number;
    total_commission: number;
    net_commission: number;
    seller_commission: number;
    shopee_commission: number;
    pending_count: number;
    pending_amount: number;
    confirmed_count: number;
    confirmed_amount: number;
    available_to_withdraw: number;
}

export interface CampaignTracking {
    id: number;
    title: string;
    channel: string;
    status: string;
    tracking_link: string;
    clicks: number;
    conversions: number;
    revenue: number;
    created_at: string;
}

export async function syncSales(days = 7) {
    const response = await api.post(`/sales/sync?days=${days}`);
    return response.data.data;
}

export async function listSales(status = ""): Promise<SaleItem[]> {
    const q = status ? `?status=${status}` : "";
    return getData<SaleItem[]>(`/sales${q}`);
}

export async function getFinancialSummary(): Promise<FinancialSummary> {
    return getData<FinancialSummary>("/sales/financial");
}

export async function getCampaignTracking(): Promise<CampaignTracking[]> {
    return getData<CampaignTracking[]>("/sales/campaigns/tracking");
}

export async function generateTrackingLink(originUrl: string, campaignId?: number) {
    return postData<{ short_link: string; long_link: string }, object>(
        "/sales/tracking-link",
        { origin_url: originUrl, campaign_id: campaignId },
    );
}
