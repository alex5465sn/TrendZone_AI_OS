from app.integrations.shopee.services.feed_service import FeedService


class FeedRepository:
    """
    Repositório responsável pelos
    Data Feeds da Shopee.
    """

    def __init__(
        self,
        service: FeedService,
    ):
        self.service = service

    def list_feeds(
        self,
        feed_mode: str | None = None,
    ):
        return self.service.list_feeds(
            feed_mode
        )

    def feed_data(
        self,
        datafeed_id: str,
        offset: int = 0,
        limit: int = 500,
    ):
        return self.service.feed_data(
            datafeed_id,
            offset,
            limit,
        )