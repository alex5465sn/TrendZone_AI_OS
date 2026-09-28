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
        "🚨 Preço despencou agora",
        "💸 Tá quase de graça",
        "😱 Não acreditei nesse preço",
        "🏷️ Achado da Shopee",
        "⏰ Só até acabar o estoque",
        "🎁 Dica do dia pra economizar",
        "🔎 Garimpo de hoje",
    ]

    _CTA = [
        "Corre que acaba rápido!",
        "Garanta o seu antes que esgote.",
        "Link direto na bio/comentário.",
        "Aproveite enquanto o preço está assim.",
        "Poucas unidades, não perde essa!",
        "Já garanti o meu. E você?",
        "Salva esse post pra não perder!",
        "Marca aqui quem precisa ver isso 👇",
        "Comenta 'EU QUERO' pra receber o link!",
        "Tá esperando o quê? Clica no link!",
        "Compartilha com quem ama uma promoção 🔥",
    ]

    _STORYTELLING = [
        "Eu testei e aprovei — olha esse preço:",
        "Uma seguidora me indicou e eu fui conferir:",
        "Vocês pediram dicas de economia? Achei esse:",
        "Tava procurando algo bom e barato e olha o que encontrei:",
        "Esse aqui é daqueles que some rápido do estoque:",
        "Não é jabá, é ACHADO mesmo:",
    ]

    _EDUCATIONAL_HOOKS = [
        "💡 Antes de comprar, vale saber disso:",
        "🤔 Um erro comum na hora de escolher:",
        "📌 Dica de quem já comprou muito por aqui:",
        "🧠 Isso pode te poupar uma compra ruim:",
    ]

    _EDUCATIONAL_TIPS = [
        "Preço baixo é ótimo, mas o que realmente importa é se o produto resolve o "
        "seu problema — vale checar avaliação e quantidade de vendas antes de decidir.",
        "Muita gente compra só pelo desconto e esquece de ver se o item serve pro "
        "uso que precisa. Vale sempre ler as avaliações reais de quem já comprou.",
        "Um jeito simples de não se arrepender: prioriza vendedores com histórico "
        "bom e nota alta, mesmo que custe um pouco mais.",
        "Antes de clicar em comprar, pergunta pra você: isso resolve o que eu "
        "preciso agora ou é só impulso? Se a resposta for sim, aí vale a pena.",
    ]

    _EDUCATIONAL_CTAS = [
        "Se fizer sentido pra você, dá uma olhada nesse aqui:",
        "Ficou com dúvida de qual escolher? Comenta aqui que te ajudo.",
        "Guarda essa dica — e, se precisar, esse aqui é uma boa opção:",
        "Vale pesquisar antes de comprar. Esse aqui passou no teste:",
    ]

    _CHANNELS = [
        "Grupo de ofertas no WhatsApp",
        "Canal de cupons no Telegram",
        "Comunidade de achadinhos no Facebook",
        "Stories/Reels no Instagram",
        "Status do WhatsApp",
        "Feed do Instagram",
        "Grupo de promoções relâmpago",
    ]

    _TONES = {
        "oferta": {
            "hooks": _HOOKS,
            "ctas": _CTA,
        },
        "storytelling": {
            "hooks": _STORYTELLING,
            "ctas": [
                "Vale muito a pena, testa também!",
                "Comenta aqui se você também ama um achado desses.",
                "Salva pra não esquecer depois.",
            ],
        },
        "humor": {
            "hooks": [
                "😂 Minha carteira não perdoou esse preço",
                "🤡 Eu resistindo até ver esse preço",
                "😅 Não é sorte, é Shopee",
            ],
            "ctas": [
                "Corre antes que o povo limpe o estoque 🏃",
                "Se não comprar hoje, amanhã já era 😭",
                "Marca o amigo pão-duro que ama economizar 👇",
            ],
        },
        "urgencia": {
            "hooks": [
                "🚨 ÚLTIMAS UNIDADES",
                "⏳ Só até acabar o estoque",
                "🔴 Preço volta a subir em breve",
            ],
            "ctas": [
                "Não deixa pra depois, pode acabar!",
                "Estoque limitado, corre lá!",
                "Agora ou nunca — clica no link!",
            ],
        },
        "educativo": {
            "hooks": _EDUCATIONAL_HOOKS,
            "ctas": _EDUCATIONAL_CTAS,
        },
    }

    # =====================================================
    # GERAÇÃO
    # =====================================================

    @classmethod
    def generate(
        cls,
        product: dict,
        tone: str = "oferta",
    ) -> dict:

        cls.log_info(
            f"Gerando conteúdo para produto {product.get('name', '')} "
            f"(tom={tone})..."
        )

        name = product.get("name", "Produto")
        price = product.get("price", 0)
        commission = product.get("commission", 0)
        rating = product.get("rating", 0)
        sales = product.get("sales", 0)

        tone_preset = cls._TONES.get(tone, cls._TONES["oferta"])
        hook = random.choice(tone_preset["hooks"])
        cta = random.choice(tone_preset["ctas"])
        story = random.choice(cls._STORYTELLING)
        channel = cls._suggest_channel(product)

        title = f"{hook}: {name}"

        stars = "⭐" * max(1, min(5, round(rating)))
        social_proof = f" | 🛒 {sales:,} vendas" if sales > 0 else ""
        price_line = f"💰 R$ {price:.2f}" if price > 0 else ""
        rating_line = f"{stars} {rating:.1f}{social_proof}" if rating > 0 else ""

        if tone == "educativo":
            tip = random.choice(cls._EDUCATIONAL_TIPS)
            opener = f"{hook}\n\n{tip}\n\n"
        else:
            use_story = random.random() < 0.5
            opener = f"{story}\n\n" if use_story else f"{hook}!\n\n"

        caption = opener + f"📦 {name}\n"
        if price_line:
            caption += f"{price_line}\n"
        if rating_line:
            caption += f"{rating_line}\n"
        caption += f"\n{cta}"

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
            "tone": tone,
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

        base = ["#achadinhos", "#oferta", "#shopee", "#promocao"]
        engagement = random.sample([
            "#dicadeeconomia", "#garimpo", "#ofertadodia",
            "#cupomshopee", "#compraonline", "#preçobaixo",
            "#economiainteligente", "#desconto", "#ficadica",
            "#trendzone", "#achado",
        ], k=3)
        extra = [f"#{w}" for w in words]

        return " ".join(base + engagement + extra)

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
