import { getData } from "./apiResponse";

export interface GoogleTrendResult {
    keyword: string;
    trend: "rising" | "stable" | "declining" | "unknown";
    interest_over_time: Record<string, number>;
    related_queries: any[];
    timestamp: string;
}

export interface ArbitrageOpportunity {
    product_name: string;
    shopee: { price: number | null; commission: number | null; link: string | null };
    mercadolivre: { price: number | null; commission: number | null; link: string | null };
    amazon: { price: number | null; commission: number | null; link: string | null };
    best_price_marketplace: string;
    price_difference_percent: number;
    opportunity_score: number;
    timestamp: string;
}

export async function getGoogleTrend(
    keyword: string,
    timeframe: string = "today 1-m",
    geo: string = "BR",
): Promise<GoogleTrendResult> {
    const qs = new URLSearchParams({ keyword, timeframe, geo }).toString();
    return getData<GoogleTrendResult>(`/trends/google-trends?${qs}`);
}

export async function getGoogleTrendsBatch(
    keywords: string[],
    timeframe: string = "today 1-m",
    geo: string = "BR",
): Promise<GoogleTrendResult[]> {
    const qs = new URLSearchParams({ keywords: keywords.join(","), timeframe, geo }).toString();
    return getData<GoogleTrendResult[]>(`/trends/google-trends/batch?${qs}`);
}

export async function getArbitrageOpportunity(
    productName: string,
    minDifference: number = 15.0,
): Promise<ArbitrageOpportunity> {
    const qs = new URLSearchParams({
        product_name: productName,
        min_difference: String(minDifference),
    }).toString();
    return getData<ArbitrageOpportunity>(`/trends/arbitrage?${qs}`);
}

export async function getArbitrageOpportunitiesBatch(
    productNames: string[],
    minDifference: number = 15.0,
): Promise<ArbitrageOpportunity[]> {
    const qs = new URLSearchParams({
        products: productNames.join(","),
        min_difference: String(minDifference),
    }).toString();
    return getData<ArbitrageOpportunity[]>(`/trends/arbitrage/batch?${qs}`);
}
