"""
TrendZone AI OS
================================

Google Trends Service

Monitora tendências de busca em tempo real
usando a API gratuita do Google Trends.
"""

import asyncio
from typing import Optional, Dict, List
from datetime import datetime, timedelta

import aiohttp
from pytrends.request import TrendReq

from app.services.base_service import BaseService


class GoogleTrendsService(BaseService):
    """
    Serviço de monitoramento de tendências do Google.
    
    Usa pytrends (wrapper não-oficial da API do Google Trends).
    Sem autenticação necessária.
    """

    SERVICE_NAME = "GOOGLE_TRENDS"

    # =====================================================
    # CACHE (em memória, 1 hora)
    # =====================================================

    _cache: Dict[str, Dict] = {}
    _cache_ttl: Dict[str, datetime] = {}

    CACHE_DURATION_MINUTES = 60

    # =====================================================
    # BUSCAR TENDÊNCIA DE UMA KEYWORD
    # =====================================================

    @classmethod
    async def get_trend(
        cls,
        keyword: str,
        timeframe: str = "today 1-m",  # últimos 30 dias
        geo: str = "BR",  # Brasil
    ) -> Optional[Dict]:
        """
        Busca tendência de uma keyword no Google Trends.

        Args:
            keyword: palavra-chave (ex: "vestido feminino")
            timeframe: período (ex: "today 1-m", "today 3-m", "today 12-m")
            geo: código do país (ex: "BR", "US")

        Returns:
            {
                "keyword": "vestido feminino",
                "trend": "rising" | "stable" | "declining",
                "interest_over_time": [...],
                "related_queries": [...],
                "timestamp": "2026-10-10T15:30:00"
            }
        """

        cls.log_info(f"Buscando tendência: {keyword}")

        # Verificar cache
        cache_key = f"{keyword}_{geo}_{timeframe}"
        if cls._is_cached(cache_key):
            cls.log_info(f"Retornando do cache: {keyword}")
            return cls._cache[cache_key]

        try:
            # Buscar do Google Trends
            pytrends = TrendReq(hl="pt-BR", tz=180)  # tz=180 é UTC-3 (Brasil)
            
            # Buscar interesse ao longo do tempo
            pytrends.build(
                kw_list=[keyword],
                timeframe=timeframe,
                geo=geo,
            )

            interest_over_time = pytrends.interest_over_time()
            related_queries = pytrends.related_queries()

            # Calcular tendência (rising/stable/declining)
            if len(interest_over_time) > 0:
                recent = interest_over_time[keyword].tail(7).mean()
                previous = interest_over_time[keyword].head(7).mean()
                
                if recent > previous * 1.1:  # 10% de aumento
                    trend = "rising"
                elif recent < previous * 0.9:  # 10% de queda
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "unknown"

            result = {
                "keyword": keyword,
                "trend": trend,
                "interest_over_time": interest_over_time[keyword].tail(7).to_dict(),
                "related_queries": related_queries.get(keyword, {}).get("top_queries", []).to_dict() if related_queries.get(keyword) else [],
                "timestamp": datetime.utcnow().isoformat(),
            }

            # Cachear resultado
            cls._cache[cache_key] = result
            cls._cache_ttl[cache_key] = datetime.utcnow() + timedelta(minutes=cls.CACHE_DURATION_MINUTES)

            cls.log_success(f"Tendência encontrada: {keyword} ({trend})")
            return result

        except Exception as e:
            cls.log_exception(f"Erro ao buscar tendência: {e}")
            return None

    # =====================================================
    # BUSCAR MÚLTIPLAS KEYWORDS
    # =====================================================

    @classmethod
    async def get_trends_batch(
        cls,
        keywords: List[str],
        timeframe: str = "today 1-m",
        geo: str = "BR",
    ) -> List[Dict]:
        """
        Busca tendências de múltiplas keywords em paralelo.
        """

        cls.log_info(f"Buscando tendências de {len(keywords)} keywords")

        tasks = [
            cls.get_trend(kw, timeframe, geo)
            for kw in keywords
        ]

        results = await asyncio.gather(*tasks)
        
        # Filtrar None
        results = [r for r in results if r is not None]

        cls.log_success(f"Tendências encontradas: {len(results)}/{len(keywords)}")
        return results

    # =====================================================
    # CALCULAR SCORE DE TENDÊNCIA
    # =====================================================

    @classmethod
    def calculate_trend_score(
        cls,
        trend: str,
    ) -> float:
        """
        Converte tendência em score 0-100.

        rising → 80-100
        stable → 40-60
        declining → 0-20
        unknown → 30
        """

        if trend == "rising":
            return 85.0
        elif trend == "stable":
            return 50.0
        elif trend == "declining":
            return 15.0
        else:
            return 30.0

    # =====================================================
    # CACHE
    # =====================================================

    @classmethod
    def _is_cached(cls, key: str) -> bool:
        """Verifica se está em cache e não expirou."""
        if key not in cls._cache:
            return False
        
        if key not in cls._cache_ttl:
            return False
        
        if datetime.utcnow() > cls._cache_ttl[key]:
            del cls._cache[key]
            del cls._cache_ttl[key]
            return False
        
        return True

    @classmethod
    def clear_cache(cls):
        """Limpa cache."""
        cls._cache.clear()
        cls._cache_ttl.clear()
        cls.log_info("Cache limpo")
