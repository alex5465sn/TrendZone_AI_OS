from app.core.settings import settings
from app.services.content_generator_service import ContentGeneratorService

PRODUCT = {
    "name": "Fone de ouvido bluetooth",
    "price": 49.9,
    "commission": 5.0,
    "rating": 4.7,
    "sales": 1200,
}


def test_generate_with_ai_returns_none_without_key(monkeypatch):
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "")
    assert ContentGeneratorService.generate_with_ai(PRODUCT) is None


def test_generate_with_ai_returns_none_on_api_error(monkeypatch):
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "fake-key")
    monkeypatch.setattr(
        "app.services.ai_agent_service.generate_reply",
        lambda **kwargs: {"ok": False, "error": "OpenRouter retornou 401"},
    )
    assert ContentGeneratorService.generate_with_ai(PRODUCT) is None


def test_generate_with_ai_returns_none_on_malformed_json(monkeypatch):
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "fake-key")
    monkeypatch.setattr(
        "app.services.ai_agent_service.generate_reply",
        lambda **kwargs: {"ok": True, "reply": "isso não é um JSON"},
    )
    assert ContentGeneratorService.generate_with_ai(PRODUCT) is None


def test_generate_with_ai_success(monkeypatch):
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "fake-key")
    fake_reply = (
        '{"hook": "Testei 5 e só 1 valeu a pena", '
        '"body": "Esse fone surpreendeu pelo custo-benefício.", '
        '"cta": "Salva esse post antes que o preço suba", '
        '"hashtags": ["achadinhos", "fone", "shopee"]}'
    )
    monkeypatch.setattr(
        "app.services.ai_agent_service.generate_reply",
        lambda **kwargs: {"ok": True, "reply": fake_reply},
    )
    content = ContentGeneratorService.generate_with_ai(PRODUCT)
    assert content is not None
    assert content["ai_generated"] is True
    assert "Testei 5 e só 1 valeu a pena" in content["caption"]
    assert "#achadinhos" in content["hashtags"]


def test_generate_smart_falls_back_when_disabled(monkeypatch):
    monkeypatch.setattr(settings, "AI_CONTENT_GENERATION_ENABLED", False)
    content = ContentGeneratorService.generate_smart(PRODUCT)
    assert "ai_generated" not in content


def test_generate_smart_falls_back_on_ai_failure(monkeypatch):
    monkeypatch.setattr(settings, "AI_CONTENT_GENERATION_ENABLED", True)
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "")
    content = ContentGeneratorService.generate_smart(PRODUCT)
    assert "ai_generated" not in content


def test_generate_smart_uses_ai_when_enabled(monkeypatch):
    monkeypatch.setattr(settings, "AI_CONTENT_GENERATION_ENABLED", True)
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "fake-key")
    fake_reply = (
        '{"hook": "Isso aqui quase saiu de linha", '
        '"body": "Poucas unidades restantes desse item.", '
        '"cta": "Comenta QUERO que te mando o link", '
        '"hashtags": ["oferta", "shopee"]}'
    )
    monkeypatch.setattr(
        "app.services.ai_agent_service.generate_reply",
        lambda **kwargs: {"ok": True, "reply": fake_reply},
    )
    content = ContentGeneratorService.generate_smart(PRODUCT)
    assert content["ai_generated"] is True
