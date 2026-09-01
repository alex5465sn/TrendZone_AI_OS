import api from "../api/axios";

export interface ApiResponse<T> {
    success: boolean;
    message: string;
    timestamp: string;
    data: T;
}

export function extractData<T>(response: { data: ApiResponse<T> }): T {
    return response.data.data;
}

export async function getData<T>(url: string): Promise<T> {
    const response = await api.get<ApiResponse<T>>(url);
    return extractData(response);
}

export async function postData<T, D>(url: string, payload: D): Promise<T> {
    const response = await api.post<ApiResponse<T>>(url, payload);
    return extractData(response);
}

export async function putData<T, D>(url: string, payload: D): Promise<T> {
    const response = await api.put<ApiResponse<T>>(url, payload);
    return extractData(response);
}

export async function deleteData<T>(url: string): Promise<T> {
    const response = await api.delete<ApiResponse<T>>(url);
    return extractData(response);
}
