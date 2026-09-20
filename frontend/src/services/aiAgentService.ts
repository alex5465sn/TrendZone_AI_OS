import { getData, putData, postData } from "./apiResponse";

export interface AIAgentConfig {
    is_enabled: boolean;
    auto_reply_whatsapp: boolean;
    provider: string;
    model_name: string;
    system_prompt: string;
    provider_configured: boolean;
    providers_disponiveis: string[];
}

export async function getAIAgentConfig() {
    return getData<AIAgentConfig>("/ai-agent/config");
}

export async function updateAIAgentConfig(payload: {
    is_enabled: boolean;
    auto_reply_whatsapp: boolean;
    provider: string;
    model_name: string;
    system_prompt: string;
}) {
    return putData<AIAgentConfig, typeof payload>("/ai-agent/config", payload);
}

export async function testAIAgent(message: string) {
    return postData<{ reply: string }, { message: string }>("/ai-agent/test", { message });
}
