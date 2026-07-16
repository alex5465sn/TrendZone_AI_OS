import api from "../api/axios";

export interface DashboardData {
    products: number;
    score: number;
    commission: number;
    ai_products: number;
}

export async function getDashboard() {
    const response = await api.get<DashboardData>("/dashboard");

    return response.data;
}