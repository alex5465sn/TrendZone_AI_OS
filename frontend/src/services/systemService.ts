import api from "../api/axios";

export async function getSystemStatus() {
    const response = await api.get("/");
    return response.data;
}