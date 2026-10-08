import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface MarketplaceAccountItem {
    id: number;
    uuid: string;
    marketplace: string;
    has_access_token: boolean;
    has_refresh_token: boolean;
    status: string;
    last_validated_at: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface ConnectPayload {
    marketplace: string;
    access_token?: string;
    refresh_token?: string;
    extra?: string;
}

export async function listAvailableMarketplaces(): Promise<string[]> {
    const data = await getData<{ marketplaces: string[] }>(
        "/marketplace-accounts/available"
    );
    return data.marketplaces;
}

export async function listMyAccounts(): Promise<MarketplaceAccountItem[]> {
    return getData<MarketplaceAccountItem[]>("/marketplace-accounts");
}

export async function connectAccount(payload: ConnectPayload) {
    return postData("/marketplace-accounts/", payload);
}

export async function disconnectAccount(marketplace: string) {
    return deleteData(`/marketplace-accounts/${marketplace}`);
}

export async function updateAccount(
    marketplace: string,
    payload: Partial<ConnectPayload>
) {
    const response = await api.patch(
        `/marketplace-accounts/${marketplace}`,
        payload
    );
    return response.data.data;
}
