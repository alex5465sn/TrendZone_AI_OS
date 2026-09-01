import { getData, postData } from "./apiResponse";

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    name: string;
    email: string;
    password: string;
    company?: string;
}

export interface AuthResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
    user: {
        id: number;
        uuid: string;
        name: string;
        email: string;
        role: string;
        plan: string;
        company: string;
        avatar: string;
    };
}

export interface UserInfo {
    id: number;
    uuid: string;
    name: string;
    email: string;
    role: string;
    plan: string;
    company: string;
    avatar: string;
    is_active: boolean;
}

const TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const USER_KEY = "user_info";

export async function register(data: RegisterRequest): Promise<AuthResponse> {
    return postData<AuthResponse, RegisterRequest>("/auth/register", data);
}

export async function login(data: LoginRequest): Promise<AuthResponse> {
    const response = await postData<AuthResponse, LoginRequest>("/auth/login", data);
    
    if (response.access_token) {
        localStorage.setItem(TOKEN_KEY, response.access_token);
        localStorage.setItem(REFRESH_TOKEN_KEY, response.refresh_token);
        localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    }
    
    return response;
}

export async function logout(): Promise<void> {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
}

export function getAccessToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
}

export function getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getUserInfo(): any | null {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
}

export function isAuthenticated(): boolean {
    return !!getAccessToken();
}

export function isAdmin(): boolean {
    const user = getUserInfo();
    return user?.role === "ADMIN";
}

export async function getCurrentUser(): Promise<UserInfo> {
    const token = getAccessToken();
    if (!token) {
        throw new Error("Não autenticado");
    }
    
    return getData<UserInfo>("/auth/me");
}

export async function refreshAccessToken(): Promise<string> {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
        throw new Error("Refresh token não disponível");
    }
    
    const response = await postData<{ access_token: string }, { refresh_token: string }>(
        "/auth/refresh",
        { refresh_token: refreshToken }
    );
    
    if (response.access_token) {
        localStorage.setItem(TOKEN_KEY, response.access_token);
    }
    
    return response.access_token;
}
