import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface ProspectDossie {
    nicho: string;
    qtd_produtos: number;
    preco_medio: number;
    comissao_media: number;
    vendas_total: number;
    score_medio_produtos: number;
    melhor_produto: string;
}

export interface Prospect {
    id: number;
    uuid: string;
    nicho: string;
    cidade: string;
    busca: string;
    nome: string;
    score: number;
    temperatura: string;
    abordagem: string;
    dossie: ProspectDossie;
    canal_sugerido: string;
    status: string;
    produto_ids: string;
    qtd_produtos: number;
    preco_medio: number;
    comissao_media: number;
    vendas_total: number;
    created_at: string;
}

export interface ScheduleItem {
    id: number;
    nicho: string;
    cidade: string;
    hora: string;
    dias: string;
    quantos: number;
    ultimo_run: string;
    status: string;
    created_at: string;
}

export async function scanProspects(nicho = ""): Promise<Prospect[]> {
    return getData<Prospect[]>(`/prospects/scan?nicho=${encodeURIComponent(nicho)}`);
}

export async function listProspects(temperatura = ""): Promise<Prospect[]> {
    const q = temperatura ? `?temperatura=${temperatura}` : "";
    return getData<Prospect[]>(`/prospects${q}`);
}

export async function updateProspectStatus(id: number, status: string) {
    const response = await api.patch(`/prospects/${id}/status?status=${encodeURIComponent(status)}`);
    return response.data.data;
}

export async function deleteProspect(id: number) {
    return deleteData(`/prospects/${id}`);
}

export async function createSchedule(payload: {
    nicho: string; cidade?: string; hora?: string; dias?: string; quantos?: number;
}) {
    return postData<{ id: number; status: string }, typeof payload>(
        "/prospects/schedules", payload,
    );
}

export async function listSchedules(): Promise<ScheduleItem[]> {
    return getData<ScheduleItem[]>("/prospects/schedules");
}

export async function deleteSchedule(id: number) {
    return deleteData(`/prospects/schedules/${id}`);
}
