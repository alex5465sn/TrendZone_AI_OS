import { getData } from "./apiResponse";
import api from "../api/axios";

export interface VocabularyConfig {
    niche_name: string;
    term_lead: string;
    term_prospect: string;
    term_customer: string;
    term_deal: string;
    term_hot: string;
    term_cold: string;
}

export async function getVocabulary(): Promise<VocabularyConfig> {
    return getData<VocabularyConfig>("/vocabulary");
}

export async function getPresets(): Promise<Record<string, VocabularyConfig>> {
    return getData<Record<string, VocabularyConfig>>("/vocabulary/presets");
}

export async function updateVocabulary(payload: VocabularyConfig) {
    const response = await api.put("/vocabulary", payload);
    return response.data.data;
}
