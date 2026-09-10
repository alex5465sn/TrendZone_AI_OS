import api from "../api/axios";

export interface AnalyzeProductPayload {
    price: number;
    sales: number;
    rating: number;
    commission: number;
    priceDiscountRate: number;
    productName: string;
}

export interface AnalyzeResult {
    decision: "MATAR" | "AJUSTAR" | "TESTAR" | "ESCALAR";
    opportunity: {
        score: number;
        status: string;
        breakdown: Record<string, { value: number; weight: number; contribution: number }>;
    };
    profit: {
        net_profit: number;
        net_margin_pct: number;
        roi_pct: number;
        breakeven_roas: number;
        max_cac: number;
        min_viable_price: number;
        ideal_price: number;
    };
    reasoning: Record<string, number>;
}

export async function analyzeProduct(product: AnalyzeProductPayload): Promise<AnalyzeResult> {
    const response = await api.post("/commercial-intelligence/analyze", { product });
    return response.data.data;
}
