import api from "../api/axios";

export interface HealthData {
    backend: string;
    database: string;
    dashboard: string;
    frontend: string;
    scout: string;
    shopee: string;
    version: string;
}

export async function getHealth() {

    const response = await api.get<HealthData>("/health");

    return response.data;

}