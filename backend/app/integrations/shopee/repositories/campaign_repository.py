from app.integrations.shopee.services.campaign_service import CampaignService


class CampaignRepository:
    """
    Repositório responsável pelas campanhas
    da Shopee.
    """

    def __init__(
        self,
        service: CampaignService,
    ):
        self.service = service

    def shop_offers(
        self,
        **filters,
    ):
        return self.service.shop_offer(
            **filters
        )

    def shopee_offers(
        self,
        **filters,
    ):
        return self.service.shopee_offer(
            **filters
        )