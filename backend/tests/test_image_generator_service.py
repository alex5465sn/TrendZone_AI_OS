from app.core.settings import settings
from app.services.image_generator_service import generate_cover_image


def test_generate_cover_image_returns_none_without_api_key(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    assert generate_cover_image("Fone de ouvido bluetooth") is None


def test_generate_cover_image_returns_none_on_api_error(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "fake-key")

    class FakeResponse:
        ok = False
        status_code = 401
        text = "invalid api key"

    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.image_generator_service.requests.post", fake_post
    )
    assert generate_cover_image("Fone de ouvido bluetooth") is None


def test_generate_cover_image_returns_none_on_exception(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "fake-key")

    def raise_error(*args, **kwargs):
        raise ConnectionError("timeout")

    monkeypatch.setattr(
        "app.services.image_generator_service.requests.post", raise_error
    )
    assert generate_cover_image("Fone de ouvido bluetooth") is None
