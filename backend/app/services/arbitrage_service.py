"""
TrendZone AI OS
================================

Arbitrage Service

Compara preços de um produto em múltiplos
marketplaces (Shopee, Mercado Livre, Amazon)
e identifica oportunidades de arbitragem.
"""

from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime

from app.services.base_service import BaseService
from app.services.shopee_service import ShopeeService
from app.services.marketplace_service import MarketplaceService


@dataclass
class ArbitrageOpportunity:
    """Oportunidade de arbitragem entre marketplaces."""
    
    product_name: str
    shopee_price: Optional[float] = None
    shopee_commission: Optional[float] = None
    shopee_link: Optional[str] = None
    
    mercadolivre_price: Optional[float] = None
    mercadolivre_commission: Optional[float] = None
    mercadolivre_link: Optional[str] = None
    
    amazon_price: Optional[float] = None
    amazon_commission: Optional[float] = None
    amazon_link: Optional[str] = None
    
    best_price_marketplace: str = ""
    price_difference_percent: float = 0.0
    opportunity_score: float = 0.0  # 0-100
    timestamp: str = ""

    def to_dict(self) -> Dict:
        return {
            "product_name": self.product_name,
            "shopee": {
                "price": self.shopee_price,
                "commission": self.shopee_commission,
                "link": self.shopee_link,
            },
            "mercadolivre": {
                "price": self.mercadolivre_price,
                "commission": self.mercadolivre_commission,
                "link": self.mercadolivre_link,
            },
            "amazon": {
                "price": self.amazon_price,
                "commission": self.amazon_commission,
                "link": self.amazon_link,
            },
            "best_price_marketplace": self.best_price_marketplace,
            "price_difference_percent": self.price_difference_percent,
            "opportunity_score": self.opportunity_score,
            "timestamp": self.timestamp,
        }


class ArbitrageService(BaseService):
    """
    Serviço de análise de arbitragem entre marketplaces.
    
    Encontra produtos que estão mais baratos em um marketplace
    e mais caros em outro — oportunidade de vender em ambos.
    """

    SERVICE_NAME = "ARBITRAGE"

    # =====================================================
    # BUSCAR OPORTUNIDADES DE ARBITRAGEM
    # =====================================================

    @classmethod
    async def find_opportunities(
        cls,
        product_name: str,
        min_price_difference_percent: float = 15.0,  # mínimo 15% de diferença
    ) -> Optional[ArbitrageOpportunity]:
        """
        Busca oportunidades de arbitragem para um produto.

        Args:
            product_name: nome do produto (ex: "vestido feminino")
            min_price_difference_percent: diferença mínima de preço (%)

        Returns:
            ArbitrageOpportunity com preços de todos os marketplaces
        """

        cls.log_info(f"Analisando arbitragem: {product_name}")

        opportunity = ArbitrageOpportunity(
            product_name=product_name,
            timestamp=datetime.utcnow().isoformat(),
        )

        # Buscar no Shopee
        try:
            shopee_result = await ShopeeService.search_products(
                keyword=product_name,
                limit=1,
            )
            if shopee_result and len(shopee_result) > 0:
                product = shopee_result[0]
                opportunity.shopee_price = product.price
                opportunity.shopee_commission = product.commission
                opportunity.shopee_link = product.offer_link
                cls.log_info(f"Shopee: R${product.price}")
        except Exception as e:
            cls.log_warning(f"Erro ao buscar Shopee: {e}")

        # Buscar no Mercado Livre
        try:
            ml_result = await MarketplaceService.search_products(
                keyword=product_name,
                limit=1,
            )
            if ml_result and len(ml_result) > 0:
                product = ml_result[0]
                opportunity.mercadolivre_price = product.price
                opportunity.mercadolivre_commission = product.commission
                opportunity.mercadolivre_link = product.offer_link
                cls.log_info(f"Mercado Livre: R${product.price}")
        except Exception as e:
            cls.log_warning(f"Erro ao buscar Mercado Livre: {e}")

        # Calcular oportunidade
        cls._calculate_opportunity(opportunity, min_price_difference_percent)

        cls.log_success(f"Análise concluída: {opportunity.opportunity_score}/100")
        return opportunity

    # =====================================================
    # CALCULAR SCORE DE OPORTUNIDADE
    # =====================================================

    @classmethod
    def _calculate_opportunity(
        cls,
        opportunity: ArbitrageOpportunity,
        min_price_difference_percent: float,
    ):
        """Calcula score de oportunidade."""

        prices = [
            opportunity.shopee_price,
            opportunity.mercadolivre_price,
            opportunity.amazon_price,
        ]

        # Filtrar None
        prices = [p for p in prices if p is not None]

        if len(prices) < 2:
            opportunity.opportunity_score = 0.0
            return

        min_price = min(prices)
        max_price = max(prices)

        price_diff_percent = ((max_price - min_price) / min_price) * 100

        # Verificar se atende mínimo
        if price_diff_percent < min_price_difference_percent:
            opportunity.opportunity_score = 0.0
            return

        # Encontrar melhor preço
        if opportunity.shopee_price == min_price:
            opportunity.best_price_marketplace = "shopee"
        elif opportunity.mercadolivre_price == min_price:
            opportunity.best_price_marketplace = "mercadolivre"
        elif opportunity.amazon_price == min_price:
            opportunity.best_price_marketplace = "amazon"

        opportunity.price_difference_percent = price_diff_percent

        # Score: quanto maior a diferença, maior o score
        # Máximo 100 em 50% de diferença
        opportunity.opportunity_score = min(
            (price_diff_percent / 50.0) * 100,
            100.0,
        )

    # =====================================================
    # BUSCAR MÚLTIPLAS OPORTUNIDADES
    # =====================================================

    @classmethod
    async def find_opportunities_batch(
        cls,
        product_names: List[str],
        min_price_difference_percent: float = 15.0,
    ) -> List[ArbitrageOpportunity]:
        """
        Busca oportunidades para múltiplos produtos.
        """

        cls.log_info(f"Analisando {len(product_names)} produtos")

        opportunities = []
        for product_name in product_names:
            try:
                opp = await cls.find_opportunities(
                    product_name,
                    min_price_difference_percent,
                )
                if opp and opp.opportunity_score > 0:
                    opportunities.append(opp)
            except Exception as e:
                cls.log_warning(f"Erro ao analisar {product_name}: {e}")

        # Ordenar por score
        opportunities.sort(
            key=lambda x: x.opportunity_score,
            reverse=True,
        )

        cls.log_success(f"Oportunidades encontradas: {len(opportunities)}")
        return opportunities
