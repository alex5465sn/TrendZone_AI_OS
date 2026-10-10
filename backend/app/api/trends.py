"""
TrendZone AI OS
================================

Trends API

Endpoints para Google Trends e Arbitragem.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services.google_trends_service import GoogleTrendsService
from app.services.arbitrage_service import ArbitrageService
from app.api.response import success_response, error_response

router = APIRouter(
    prefix="/api/trends",
    tags=["trends"],
)


# =====================================================
# GOOGLE TRENDS
# =====================================================

@router.get("/google-trends")
async def get_google_trends(
    keyword: str = Query(..., description="Palavra-chave para buscar"),
    timeframe: str = Query("today 1-m", description="Período (today 1-m, today 3-m, today 12-m)"),
    geo: str = Query("BR", description="Código do país (BR, US, etc)"),
    current_user = Depends(get_current_user),
):
    """
    Busca tendência de uma keyword no Google Trends.

    Retorna:
    - trend: rising | stable | declining
    - interest_over_time: interesse ao longo do tempo
    - related_queries: queries relacionadas
    """

    try:
        result = await GoogleTrendsService.get_trend(
            keyword=keyword,
            timeframe=timeframe,
            geo=geo,
        )

        if not result:
            return error_response(
                "Não foi possível buscar tendência",
                status_code=404,
            )

        return success_response(
            data=result,
            message=f"Tendência de '{keyword}': {result['trend']}",
        )

    except Exception as e:
        return error_response(
            f"Erro ao buscar tendência: {str(e)}",
            status_code=500,
        )


@router.get("/google-trends/batch")
async def get_google_trends_batch(
    keywords: str = Query(..., description="Keywords separadas por vírgula"),
    timeframe: str = Query("today 1-m", description="Período"),
    geo: str = Query("BR", description="Código do país"),
    current_user = Depends(get_current_user),
):
    """
    Busca tendências de múltiplas keywords.
    """

    try:
        keyword_list = [kw.strip() for kw in keywords.split(",")]

        results = await GoogleTrendsService.get_trends_batch(
            keywords=keyword_list,
            timeframe=timeframe,
            geo=geo,
        )

        return success_response(
            data=results,
            message=f"Tendências encontradas: {len(results)}/{len(keyword_list)}",
        )

    except Exception as e:
        return error_response(
            f"Erro ao buscar tendências: {str(e)}",
            status_code=500,
        )


# =====================================================
# ARBITRAGEM
# =====================================================

@router.get("/arbitrage")
async def get_arbitrage(
    product_name: str = Query(..., description="Nome do produto"),
    min_difference: float = Query(15.0, description="Diferença mínima de preço (%)"),
    current_user = Depends(get_current_user),
):
    """
    Busca oportunidades de arbitragem para um produto.

    Compara preços em Shopee, Mercado Livre e Amazon.

    Retorna:
    - best_price_marketplace: marketplace com melhor preço
    - price_difference_percent: diferença de preço (%)
    - opportunity_score: score 0-100
    """

    try:
        opportunity = await ArbitrageService.find_opportunities(
            product_name=product_name,
            min_price_difference_percent=min_difference,
        )

        if not opportunity:
            return error_response(
                "Não foi possível analisar arbitragem",
                status_code=404,
            )

        return success_response(
            data=opportunity.to_dict(),
            message=f"Oportunidade: {opportunity.opportunity_score}/100",
        )

    except Exception as e:
        return error_response(
            f"Erro ao analisar arbitragem: {str(e)}",
            status_code=500,
        )


@router.get("/arbitrage/batch")
async def get_arbitrage_batch(
    products: str = Query(..., description="Produtos separados por vírgula"),
    min_difference: float = Query(15.0, description="Diferença mínima (%)"),
    current_user = Depends(get_current_user),
):
    """
    Busca oportunidades de arbitragem para múltiplos produtos.
    """

    try:
        product_list = [p.strip() for p in products.split(",")]

        opportunities = await ArbitrageService.find_opportunities_batch(
            product_names=product_list,
            min_price_difference_percent=min_difference,
        )

        return success_response(
            data=[opp.to_dict() for opp in opportunities],
            message=f"Oportunidades encontradas: {len(opportunities)}",
        )

    except Exception as e:
        return error_response(
            f"Erro ao analisar arbitragem: {str(e)}",
            status_code=500,
        )
