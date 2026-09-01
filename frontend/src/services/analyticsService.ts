import { getData } from "./apiResponse";

export interface ProductSummary {
    total_products: number;
    average_score: number;
    average_commission: number;
    average_rating: number;
    total_sales: number;
}

export interface CommissionSummary {
    total_commission: number;
    average_commission_per_product: number;
    total_products: number;
}

export interface SalesSummary {
    total_sales: number;
    average_sales_per_product: number;
    total_products: number;
}

export interface ScoreDistribution {
    "80-100": number;
    "60-79": number;
    "40-59": number;
    "0-39": number;
}

export interface CommissionDistribution {
    "0-5%": number;
    "5-10%": number;
    "10-15%": number;
    "15-20%": number;
    "20%+": number;
}

export interface TopProduct {
    id: number;
    name: string;
    score: number;
    commission: number;
    sales: number;
    rating: number;
}

export async function getProductsSummary(): Promise<ProductSummary> {
    return getData<ProductSummary>("/analytics/products/summary");
}

export async function getProductsByScore(): Promise<ScoreDistribution> {
    return getData<ScoreDistribution>("/analytics/products/by-score");
}

export async function getProductsByCommission(): Promise<CommissionDistribution> {
    return getData<CommissionDistribution>("/analytics/products/by-commission");
}

export async function getTopProducts(): Promise<TopProduct[]> {
    return getData<TopProduct[]>("/analytics/products/top-10");
}

export async function getCommissionSummary(): Promise<CommissionSummary> {
    return getData<CommissionSummary>("/analytics/commission/summary");
}

export async function getSalesSummary(): Promise<SalesSummary> {
    return getData<SalesSummary>("/analytics/sales/summary");
}

export async function getSalesByRating(): Promise<Record<string, number>> {
    return getData<Record<string, number>>("/analytics/sales/by-rating");
}
