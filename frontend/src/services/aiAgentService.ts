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

export const PROVIDER_LABELS: Record<string, string> = {
    abacus: "Abacus.AI",
    openrouter: "OpenRouter",
    openai: "OpenAI",
    anthropic: "Anthropic",
};

export const PROVIDER_MODELS: Record<string, string[]> = {
    abacus: ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"],
    openrouter: ["openai/gpt-4o-mini", "openai/gpt-4-turbo", "anthropic/claude-3-opus"],
    openai: ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    anthropic: ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
};

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
