import { getData } from "./apiResponse";

export interface DashboardStats {
    total_products: number;
    version: string;
    status: string;
    pipeline: string;
}

export interface MarketplaceSummary {
    products: number;
    shops: number;
    offers: number;
}

export async function getDashboard(): Promise<DashboardStats> {
    return getData<DashboardStats>("/dashboard");
}

export async function getHealth(): Promise<Record<string, string>> {
    return getData<Record<string, string>>("/health");
}
