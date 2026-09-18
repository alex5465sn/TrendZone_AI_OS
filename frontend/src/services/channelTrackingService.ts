import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface ChannelTrackingItem {
    id: number;
    product_id: number | null;
    channel: string;
    sub_id: string;
    tracking_url: string;
    clicks: number;
    conversions: number;
    revenue: number;
    ctr: number;
    created_at: string | null;
}

export interface ChannelSummary {
    channel: string;
    total_clicks: number;
    total_conversions: number;
    total_revenue: number;
    total_links: number;
    avg_ctr: number;
}

export async function getChannels() {
    return getData<{ id: string; name: string; icon: string }[]>("/channel-tracking/channels");
}

export async function listTrackings(channel?: string): Promise<ChannelTrackingItem[]> {
    const qs = channel ? `?channel=${channel}` : "";
    return getData<ChannelTrackingItem[]>(`/channel-tracking${qs}`);
}

export async function getChannelSummary(): Promise<ChannelSummary[]> {
    return getData<ChannelSummary[]>("/channel-tracking/summary");
}

export async function createTracking(payload: {
    channel: string;
    sub_id: string;
    product_id?: number | null;
    tracking_url?: string;
}) {
    return postData<{ id: number; sub_id: string }, typeof payload>("/channel-tracking", payload);
}

export async function updateTracking(id: number, payload: {
    clicks?: number;
    conversions?: number;
    revenue?: number;
}) {
    const response = await api.patch(`/channel-tracking/${id}`, payload);
    return response.data.data;
}

export async function deleteTracking(id: number) {
    return deleteData(`/channel-tracking/${id}`);
}
