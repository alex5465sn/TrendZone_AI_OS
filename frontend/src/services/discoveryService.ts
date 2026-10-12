import { getData } from "./apiResponse";

export interface DiscoveryProduct {
    id: number;
    name: string;
    image: string;
    price: number;
    commission: number;
    rating: number;
    sales: number;
    score: number;
    offer_link: string;
    opportunity_index?: number;
    heat_index?: number;
    tag?: string;
    recommendation?: string;
    created_at?: string;
}

export async function getEmergingProducts(params?: Record<string, any>): Promise<DiscoveryProduct[]> {
    const qs = params ? "?" + new URLSearchParams(params as any).toString() : "";
    return getData<DiscoveryProduct[]>(`/discovery/emerging${qs}`);
}

export async function getHighCommissionProducts(minCommission = 20): Promise<DiscoveryProduct[]> {
    return getData<DiscoveryProduct[]>(`/discovery/high-commission?min_commission=${minCommission}`);
}

export async function getTrendingProducts(): Promise<DiscoveryProduct[]> {
    return getData<DiscoveryProduct[]>("/discovery/trending");
}

export async function getSmartRecommendations() {
    return getData<{
        emerging: DiscoveryProduct[];
        top_performers: DiscoveryProduct[];
        high_profit: DiscoveryProduct[];
    }>("/discovery/recommendations");
}

export async function getNicheGaps() {
    return getData<any[]>("/discovery/niche-gaps");
}

export interface RadarItem extends DiscoveryProduct {
    marketplace: string;
    momentum_pct: number | null;
    price_change_pct: number | null;
    trend: "up" | "down" | "flat" | "sem_base";
    trend_signal: "rising" | "stable" | "declining" | "unknown" | null;
    radar_score: number;
    reasons: string[];
}

export async function getProductRadar(limit = 20): Promise<RadarItem[]> {
    return getData<RadarItem[]>(`/discovery/radar?limit=${limit}`);
}
