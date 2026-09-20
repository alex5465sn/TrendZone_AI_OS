"""
Serviço do Agente de IA.

Gera respostas automáticas usando um provedor de LLM configurado
via variáveis de ambiente (OpenRouter, OpenAI ou Anthropic).

Se nenhuma chave estiver configurada, retorna um aviso claro em vez
de falhar silenciosamente ou inventar uma resposta.
"""

import requests

from app.core.settings import settings


PROVIDER_LABELS = {
    "abacus": "Abacus.AI",
    "openrouter": "OpenRouter",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
}


def provider_label(provider: str) -> str:
    return PROVIDER_LABELS.get(provider, provider)


def is_provider_configured(provider: str) -> bool:
    if provider == "abacus":
        return bool(settings.ABACUS_API_KEY)
    if provider == "openrouter":
        return bool(settings.OPENROUTER_API_KEY)
    if provider == "openai":
        return bool(settings.OPENAI_API_KEY)
    if provider == "anthropic":
        return bool(settings.ANTHROPIC_API_KEY)
    return False


def generate_reply(
    provider: str,
    model_name: str,
    system_prompt: str,
    user_message: str,
    history: list[dict] | None = None,
) -> dict:
    if not is_provider_configured(provider):
        return {
            "ok": False,
            "error": f"Provedor '{provider_label(provider)}' sem chave de API configurada no .env do servidor.",
        }

    messages = [{"role": "system", "content": system_prompt}]
    for item in (history or [])[-10:]:
        messages.append(item)
    messages.append({"role": "user", "content": user_message})

    if provider == "abacus":
        return _call_abacus(model_name, messages)
    if provider == "openrouter":
        return _call_openrouter(model_name, messages)
    if provider == "openai":
        return _call_openai(model_name, messages)
    if provider == "anthropic":
        return _call_anthropic(model_name, messages)

    return {"ok": False, "error": f"Provedor '{provider}' não suportado."}


def _call_openrouter(model_name: str, messages: list[dict]) -> dict:
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": model_name, "messages": messages},
            timeout=30,
        )
        if not resp.ok:
            return {"ok": False, "error": f"OpenRouter retornou {resp.status_code}: {resp.text[:300]}"}
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        return {"ok": True, "reply": reply}
    except (requests.RequestException, KeyError, IndexError) as e:
        return {"ok": False, "error": str(e)}


def _call_openai(model_name: str, messages: list[dict]) -> dict:
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": model_name, "messages": messages},
            timeout=30,
        )
        if not resp.ok:
            return {"ok": False, "error": f"OpenAI retornou {resp.status_code}: {resp.text[:300]}"}
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        return {"ok": True, "reply": reply}
    except (requests.RequestException, KeyError, IndexError) as e:
        return {"ok": False, "error": str(e)}


def _call_anthropic(model_name: str, messages: list[dict]) -> dict:
    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    conversation = [m for m in messages if m["role"] != "system"]
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": model_name,
                "system": system,
                "messages": conversation,
                "max_tokens": 1024,
            },
            timeout=30,
        )
        if not resp.ok:
            return {"ok": False, "error": f"Anthropic retornou {resp.status_code}: {resp.text[:300]}"}
        data = resp.json()
        reply = data["content"][0]["text"]
        return {"ok": True, "reply": reply}
    except (requests.RequestException, KeyError, IndexError) as e:
        return {"ok": False, "error": str(e)}


def _call_abacus(model_name: str, messages: list[dict]) -> dict:
    try:
        resp = requests.post(
            "https://routellm.abacus.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.ABACUS_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"model": model_name, "messages": messages},
            timeout=30,
        )
        if not resp.ok:
            return {"ok": False, "error": f"Abacus.AI retornou {resp.status_code}: {resp.text[:300]}"}
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        return {"ok": True, "reply": reply}
    except (requests.RequestException, KeyError, IndexError) as e:
        return {"ok": False, "error": str(e)}
