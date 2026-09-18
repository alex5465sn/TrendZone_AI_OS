import { getData, postData, deleteData } from "./apiResponse";
import api from "../api/axios";

export interface AutomationRuleItem {
    id: number;
    name: string;
    trigger_type: string;
    trigger_config: Record<string, any>;
    action_type: string;
    action_config: Record<string, any>;
    is_enabled: boolean;
    last_triggered_at: string | null;
    trigger_count: number;
}

export interface DefinitionItem {
    id: string;
    name: string;
    config: string[];
}

export async function getDefinitions() {
    return getData<{ triggers: DefinitionItem[]; actions: DefinitionItem[] }>("/automation/definitions");
}

export async function listRules(): Promise<AutomationRuleItem[]> {
    return getData<AutomationRuleItem[]>("/automation/rules");
}

export async function createRule(payload: {
    name: string;
    trigger_type: string;
    trigger_config: Record<string, any>;
    action_type: string;
    action_config: Record<string, any>;
    is_enabled?: boolean;
}) {
    return postData<{ id: number; name: string }, typeof payload>("/automation/rules", payload);
}

export async function updateRule(id: number, payload: { is_enabled?: boolean }) {
    const response = await api.patch(`/automation/rules/${id}`, payload);
    return response.data.data;
}

export async function deleteRule(id: number) {
    return deleteData(`/automation/rules/${id}`);
}

export async function runAutomation() {
    return postData<{ executions: any[]; total: number }, {}>("/automation/run", {});
}
