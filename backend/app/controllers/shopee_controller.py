from app.integrations.shopee.services.product_service import (
    ProductService,
)

from app.integrations.shopee.services.campaign_service import (
    CampaignService,
)

from app.integrations.shopee.services.report_service import (
    ReportService,
)

from app.integrations.shopee.services.link_service import (
    LinkService,
)

from app.integrations.shopee.services.feed_service import (
    FeedService,
)

from app.integrations.shopee.repositories.product_repository import (
    ProductRepository,
)

from app.integrations.shopee.repositories.campaign_repository import (
    CampaignRepository,
)

from app.integrations.shopee.repositories.report_repository import (
    ReportRepository,
)

from app.integrations.shopee.repositories.link_repository import (
    LinkRepository,
)

from app.integrations.shopee.repositories.feed_repository import (
    FeedRepository,
)


class ShopeeController:
    """
    Controller principal da integração Shopee.
    """

    def __init__(
        self,
        token: str,
    ):

        self.products = ProductRepository(
            ProductService(
                access_token=token,
            )
        )

        self.campaigns = CampaignRepository(
            CampaignService(
                access_token=token,
            )
        )

        self.reports = ReportRepository(
            ReportService(
                access_token=token,
            )
        )

        self.links = LinkRepository(
            LinkService(
                access_token=token,
            )
        )

        self.feeds = FeedRepository(
            FeedService(
                access_token=token,
            )
        )