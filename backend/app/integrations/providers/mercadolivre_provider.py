"""
TrendZone AI OS
================================

Mercado Livre Provider

Implementação oficial do Provider
do Mercado Livre.

Observações:

- Busca de produtos usa a API pública
  do catálogo (não exige OAuth).
- O programa ML Afiliados NÃO possui
  API oficial de links de afiliado nem
  de relatório de conversões — os links
  de rastreio do TrendZone (/go/{code})
  fazem o tracking de cliques, e as
  comissões são acompanhadas no painel
  ML Afiliados.
"""

from app.integrations.providers.base_provider import BaseProvider
from app.integrations.mercadolivre.service import MercadoLivreService


class MercadoLivreProvider(BaseProvider):

    def __init__(self):

        self.service = MercadoLivreService()

    # =====================================================
    # PRODUCTS
    # =====================================================

    def search_products(self, **kwargs):

        return self.service.search_products(**kwargs)

    # =====================================================
    # SHOPS
    # =====================================================

    def search_shops(self, **kwargs):

        # A API do ML não possui busca de lojas
        # equivalente à da Shopee. Devolvemos
        # resposta vazia no mesmo formato para
        # não quebrar o contrato da UI.

        return {
            "nodes": [],
            "pageInfo": {
                "page": int(kwargs.get("page") or 1),
                "limit": int(kwargs.get("limit") or 20),
                "hasNextPage": False,
                "scrollId": "",
            },
        }

    # =====================================================
    # OFFERS
    # =====================================================

    def search_offers(self, **kwargs):

        # Reaproveita a busca do catálogo (o ML
        # não separa "ofertas" em endpoint público).

        return self.service.search_products(**kwargs)

    # =====================================================
    # SHORT LINK
    # =====================================================

    def generate_short_link(
        self,
        url: str,
        sub_ids=None,
    ):
        """
        O ML não possui API de short link de afiliado.

        O rastreamento é feito pelo encurtador próprio
        do TrendZone (/go/{tracking_code}) — ver
        POST /marketplace/promote. Aqui apenas
        devolvemos a própria URL recebida.
        """

        return {
            "short_link": url,
            "source_url": url,
            "sub_ids": sub_ids or [],
            "provider": "trendzone_tracker",
        }

    # =====================================================
    # REPORT
    # =====================================================

    def conversion_report(self, **kwargs):

        raise ValueError(
            "O Mercado Livre não possui API de relatório de "
            "conversões para afiliados. As comissões devem ser "
            "acompanhadas no painel do programa ML Afiliados."
        )
