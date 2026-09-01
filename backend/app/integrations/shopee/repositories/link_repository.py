from app.integrations.shopee.services.link_service import LinkService


class LinkRepository:
    """
    Repositório responsável pelos links
    de afiliado.
    """

    def __init__(
        self,
        service: LinkService,
    ):
        self.service = service

    def short_link(
        self,
        origin_url: str,
        sub_ids: list[str] | None = None,
    ):
        return self.service.generate_short_link(
            original_url=origin_url,
        )

    def batch_short_link(
        self,
        links: list[dict],
    ):
        return self.service.generate_batch_short_link(
            urls=links,
        )