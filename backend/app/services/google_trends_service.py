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
        cache_key = cls._cache_key(keyword, geo, timeframe)
        if cls._is_cached(cache_key):
            cls.log_info(f"Retornando do cache: {keyword}")
            return cls._cache[cache_key]

        try:
            # pytrends faz chamadas HTTP bloqueantes (biblioteca síncrona).
            # Rodar em thread separada evita travar o event loop do FastAPI
            # enquanto espera a resposta do Google.
            interest_over_time, related_queries = await asyncio.to_thread(
                cls._fetch_from_google, keyword, timeframe, geo
            )

            # Calcular tendência (rising/stable/declining)
            series = (
                interest_over_time.get(keyword)
                if interest_over_time is not None
                else None
            )
            trend = cls._trend_from_series(series)

            result = {
                "keyword": keyword,
                "trend": trend,
                "interest_over_time": cls._series_to_json_safe(
                    interest_over_time[keyword].tail(7)
                ),
                "related_queries": cls._extract_related_queries(related_queries, keyword),
                "timestamp": datetime.utcnow().isoformat(),
            }

            # Cachear resultado
            cls._cache[cache_key] = result
            cls._cache_ttl[cache_key] = datetime.utcnow() + timedelta(minutes=cls.CACHE_DURATION_MINUTES)

            cls.log_success(f"Tendência encontrada: {keyword} ({trend})")
            return result

        except Exception as e:
            cls.log_error(f"Erro ao buscar tendência: {e}")
            return None

    # =====================================================
    # CHAMADA BLOQUEANTE AO GOOGLE (roda em thread via asyncio.to_thread)
    # =====================================================

    @staticmethod
    def _fetch_from_google(keyword: str, timeframe: str, geo: str):
        pytrends = TrendReq(hl="pt-BR", tz=180)  # tz=180 é UTC-3 (Brasil)
        pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
        return pytrends.interest_over_time(), pytrends.related_queries()

    # =====================================================
    # SINAL DE TENDÊNCIA SÍNCRONO EM LOTE (para código sync)
    # =====================================================

    # Limite por requisição do Google Trends (pytrends).
    TREND_KEYWORDS_PER_REQUEST = 5

    @classmethod
    def get_trend_signal_sync(
        cls,
        keywords: List[str],
        timeframe: str = "today 1-m",
        geo: str = "BR",
    ) -> Dict[str, str]:
        """
        Sinal de tendência (rising/stable/declining) de várias keywords,
        de forma SÍNCRONA e em lote — para uso em código não-async que já
        roda em threadpool do FastAPI (ex.: MomentumService.radar).

        - Compartilha o mesmo cache de 1h do get_trend.
        - 1 requisição pytrends por grupo de até 5 keywords.
        - Nunca propaga exceção: keyword com falha volta como "unknown".
        """
        signals: Dict[str, str] = {}
        pending: List[str] = []

        for kw in keywords:
            if not kw:
                continue

            cache_key = cls._cache_key(kw, geo, timeframe)

            if cls._is_cached(cache_key):
                signals[kw] = cls._cache[cache_key].get("trend", "unknown")
            else:
                pending.append(kw)

        now = datetime.utcnow()

        for i in range(0, len(pending), cls.TREND_KEYWORDS_PER_REQUEST):
            chunk = pending[i : i + cls.TREND_KEYWORDS_PER_REQUEST]

            try:
                pytrends = TrendReq(hl="pt-BR", tz=180)
                pytrends.build_payload(chunk, timeframe=timeframe, geo=geo)
                interest_over_time = pytrends.interest_over_time()

                for kw in chunk:
                    series = (
                        interest_over_time.get(kw)
                        if interest_over_time is not None
                        else None
                    )
                    trend = cls._trend_from_series(series)

                    cache_key = cls._cache_key(kw, geo, timeframe)
                    cls._cache[cache_key] = {
                        "keyword": kw,
                        "trend": trend,
                        "interest_over_time": {},
                        "related_queries": [],
                        "timestamp": now.isoformat(),
                    }
                    cls._cache_ttl[cache_key] = now + timedelta(
                        minutes=cls.CACHE_DURATION_MINUTES
                    )

                    signals[kw] = trend

            except Exception as e:
                cls.log_error(
                    f"Erro ao buscar lote de tendências "
                    f"({len(chunk)} keywords): {e}"
                )

                for kw in chunk:
                    signals[kw] = "unknown"

        return signals

    # =====================================================
    # HELPERS DE TENDÊNCIA
    # =====================================================

    @staticmethod
    def _cache_key(keyword: str, geo: str, timeframe: str) -> str:
        return f"{keyword}_{geo}_{timeframe}"

    @staticmethod
    def _trend_from_series(series) -> str:
        """
        Classifica a tendência comparando a média da última semana
        com a primeira semana da série (+/- 10%).
        """
        if series is None:
            return "unknown"

        # Keywords sem dados no Google voltam como NaN (não como
        # série vazia) — precisa descartar antes de classificar.
        clean = series.dropna()

        if len(clean) == 0:
            return "unknown"

        recent = clean.tail(7).mean()
        previous = clean.head(7).mean()

        if recent > previous * 1.1:  # 10% de aumento
            return "rising"

        if recent < previous * 0.9:  # 10% de queda
            return "declining"

        return "stable"

    # =====================================================
    # EXTRAIR QUERIES RELACIONADAS (com segurança)
    # =====================================================

    @staticmethod
    def _extract_related_queries(related_queries: Dict, keyword: str) -> List[Dict]:
        """
        Extrai a lista de queries relacionadas em alta ("rising") retornada
        pelo pytrends. As chaves reais da resposta são "top" e "rising"
        (cada uma é um DataFrame do pandas ou None) — nunca "top_queries".
        """
        entry = related_queries.get(keyword) if related_queries else None
        if not entry:
            return []

        df = entry.get("rising")
        if df is None or df.empty:
            df = entry.get("top")

        if df is None or df.empty:
            return []

        return [
            {str(k): GoogleTrendsService._json_safe_value(v) for k, v in rec.items()}
            for rec in df.to_dict("records")
        ]

    # =====================================================
    # CONVERSÃO JSON-SAFE (numpy / pandas -> tipos nativos)
    # =====================================================

    @staticmethod
    def _json_safe_value(value):
        """Converte escalares numpy e Timestamps em tipos serializáveis por JSON."""
        if hasattr(value, "isoformat"):  # pandas.Timestamp / datetime
            return value.isoformat()
        if hasattr(value, "item"):  # numpy.int64 / float64 / bool_
            return value.item()
        return value

    @staticmethod
    def _series_to_json_safe(series) -> Dict[str, float]:
        """Converte uma Series do pandas em dict com chaves ISO e valores nativos."""
        return {
            (
                idx.isoformat()
                if hasattr(idx, "isoformat")
                else str(idx)
            ): GoogleTrendsService._json_safe_value(val)
            for idx, val in series.items()
        }

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
