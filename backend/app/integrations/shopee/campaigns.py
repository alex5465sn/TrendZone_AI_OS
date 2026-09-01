from app.integrations.shopee.gateway import ShopeeGateway


class ShopeeCampaigns:
    """
    Operações relacionadas às campanhas da Shopee.
    """

    def __init__(
        self,
        gateway: ShopeeGateway,
    ):
        self.gateway = gateway

    def get_campaigns(self):

        return self.gateway.execute(
            query="",
            variables={},
        )

    def get_campaign(
        self,
        campaign_id: int,
    ):

        return self.gateway.execute(
            query="",
            variables={
                "campaignId": campaign_id,
            },
        )