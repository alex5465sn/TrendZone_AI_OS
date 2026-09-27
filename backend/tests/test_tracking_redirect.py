"""
Testes do fluxo de tracking de cliques (/tracking, /go/{codigo}).

Este e o fluxo que estava silenciosamente quebrado em producao
devido ao APP_BASE_URL nao configurado no servidor (todos os
links gerados apontavam para localhost). Estes testes travam o
comportamento correto para evitar regressao futura.
"""

from app.api.published_posts import _build_tracking_url, redirect_tracking
from app.models.published_post import PublishedPost
from app.repositories.published_post_repository import PublishedPostRepository


def _make_post(db_session, tracking_code: str = "abc12345") -> PublishedPost:
    post = PublishedPost(
        tracking_code=tracking_code,
        product_item_id=1,
        product_name="Produto Teste",
        destination_url="https://s.shopee.com.br/exemplo",
        channel="facebook",
        post_format="texto",
        message="",
        click_count=0,
    )
    PublishedPostRepository.create(db_session, post)
    return post


def test_build_tracking_url_uses_configured_base_url():
    url = _build_tracking_url("https://api.trendzone.app", "abc123")
    assert url == "https://api.trendzone.app/go/abc123"


def test_build_tracking_url_strips_trailing_slash():
    url = _build_tracking_url("https://api.trendzone.app/", "abc123")
    assert url == "https://api.trendzone.app/go/abc123"


def test_redirect_tracking_increments_click_count_and_redirects(db_session):
    post = _make_post(db_session)

    response = redirect_tracking(post.tracking_code, db_session)

    assert response.status_code == 302
    assert response.headers["location"] == post.destination_url

    updated = PublishedPostRepository.get_by_tracking_code(db_session, post.tracking_code)
    assert updated.click_count == 1

    redirect_tracking(post.tracking_code, db_session)
    updated = PublishedPostRepository.get_by_tracking_code(db_session, post.tracking_code)
    assert updated.click_count == 2


def test_redirect_tracking_unknown_code_returns_error(db_session):
    response = redirect_tracking("nao-existe", db_session)

    assert response.status_code == 404
