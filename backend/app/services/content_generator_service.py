"""
TrendZone AI OS
================================

Content Generator Service

Responsável por gerar automaticamente
conteúdo de divulgação (título, legenda,
hashtags, público-alvo e canal sugerido)
para um produto.

Não publica nem envia nada — apenas gera
o material para que um humano revise e
publique/envie manualmente.
"""

import random

from app.services.base_service import BaseService


class ContentGeneratorService(BaseService):
    """
    Gerador de conteúdo de vendas do
    TrendZone AI OS.
    """

    SERVICE_NAME = "CONTENT_GENERATOR"

    _HOOKS = [
        "🔥 Oferta imperdível",
        "⚡ Achadinho do dia",
        "💥 Promoção relâmpago",
        "✨ Queridinho da galera",
        "🎯 Custo-benefício absurdo",
    ]

    _CTA = [
        "Corre que acaba rápido!",
        "Garanta o seu antes que esgote.",
        "Link direto na bio/comentário.",
        "Aproveite enquanto o preço está assim.",
        "Poucas unidades, não perde essa!",
    ]

    _CHANNELS = [
        "Grupo de ofertas no WhatsApp",
        "Canal de cupons no Telegram",
        "Comunidade de achadinhos no Facebook",
        "Stories/Reels no Instagram",
        "Grupo de promoções relâmpago",
    ]

    # =====================================================
    # GERAÇÃO
    # =====================================================

    @classmethod
    def generate(
        cls,
        product: dict,
    ) -> dict:

        cls.log_info(
            f"Gerando conteúdo para produto {product.get('name', '')}..."
        )

        name = product.get("name", "Produto")
        price = product.get("price", 0)
        commission = product.get("commission", 0)
        rating = product.get("rating", 0)
        sales = product.get("sales", 0)

        hook = random.choice(cls._HOOKS)
        cta = random.choice(cls._CTA)
        channel = cls._suggest_channel(product)

        title = f"{hook}: {name}"

        caption = (
            f"{hook}!\n\n"
            f"{name}\n"
            f"💰 De olho no preço: R$ {price:.2f}\n"
            f"⭐ Avaliação: {rating:.1f} | 🛒 {sales} vendas\n\n"
            f"{cta}"
        )

        hashtags = cls._build_hashtags(name)

        audience = cls._suggest_audience(product)

        cls.log_success("Conteúdo gerado com sucesso.")

        return {
            "title": title,
            "caption": caption,
            "hashtags": hashtags,
            "target_audience": audience,
            "channel": channel,
            "estimated_commission": commission,
        }

    # =====================================================
    # HASHTAGS
    # =====================================================

    @classmethod
    def _build_hashtags(
        cls,
        name: str,
    ) -> str:

        words = [
            w.lower()
            for w in name.split()
            if len(w) > 3
        ][:3]

        base = ["#promocao", "#achadinhos", "#oferta", "#shopee"]

        extra = [f"#{w}" for w in words]

        return " ".join(base + extra)

    # =====================================================
    # PÚBLICO-ALVO
    # =====================================================

    @classmethod
    def _suggest_audience(
        cls,
        product: dict,
    ) -> str:

        price = product.get("price", 0)

        if price <= 30:
            return "Compradores de baixo ticket / impulso (achadinhos)"

        if price <= 100:
            return "Público geral em busca de custo-benefício"

        return "Público de maior poder aquisitivo / itens premium"

    # =====================================================
    # CANAL SUGERIDO
    # =====================================================

    @classmethod
    def _suggest_channel(
        cls,
        product: dict,
    ) -> str:

        score = product.get("score", 0)

        if score >= 80:
            return cls._CHANNELS[0]

        if score >= 60:
            return cls._CHANNELS[1]

        return random.choice(cls._CHANNELS)
