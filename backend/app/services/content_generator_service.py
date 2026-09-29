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

import json
import random

from app.core.settings import settings
from app.services import ai_agent_service
from app.services.base_service import BaseService

AI_SYSTEM_PROMPT = """Você é um redator especialista em copywriting para posts de \
divulgação de produtos afiliados da Shopee (achadinhos, ofertas). Sua tarefa é \
escrever um HOOK (gancho), um CORPO curto e uma CTA (chamada para ação) em \
português do Brasil, para o produto informado pelo usuário.

REGRAS PARA O HOOK (primeira linha, gera o "para de rolar o feed"):
- PROIBIDO usar aberturas genéricas e batidas, ex: "Confira essa oferta incrível", \
"Não perca essa promoção", "Olha que produto legal".
- PROIBIDO frases passivas/óbvias, ex: "Você sabia que...".
- PREFIRA viés de negatividade/urgência real, ex: "Para de comprar isso errado", \
"Isso aqui quase saiu de linha".
- PREFIRA curiosidade e especificidade concreta (número, resultado, comparação), \
ex: "Testei 5 desses e só 1 valeu a pena", "Achei por menos da metade do preço normal".
- O hook deve ter no máximo ~60 caracteres e provocar uma reação de "Espera, o quê?".

REGRAS PARA A CTA (chamada final, gera a ação):
- PROIBIDO CTAs vazias, ex: "Espero que tenham gostado!", "Link na bio" sozinho.
- PREFIRA imperativo + benefício direto, ex: "Salva esse post antes que o preço suba", \
"Comenta 'QUERO' que te mando o link", "Clica agora, o estoque é curto".
- A CTA deve deixar claro o próximo passo E o benefício de tomar essa ação.

FORMATO DE SAÍDA:
Responda APENAS com um JSON válido, sem markdown, sem texto fora do JSON, no \
formato exato:
{"hook": "...", "body": "...", "cta": "...", "hashtags": ["...", "...", "..."]}

- "hook": a primeira linha, seguindo as regras acima.
- "body": 1 a 3 frases curtas destacando o produto (pode citar preço, avaliação \
ou vendas se fizerem sentido), tom natural, sem exagero de emojis.
- "cta": a chamada final, seguindo as regras acima.
- "hashtags": lista de 6 a 8 hashtags em português, sem espaços, relevantes ao \
produto e ao nicho de achadinhos/ofertas.
"""


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
    # GERAÇÃO INTELIGENTE (IA com fallback pro template)
    # =====================================================

    @classmethod
    def generate_smart(
        cls,
        product: dict,
        tone: str = "oferta",
    ) -> dict:
        """
        Tenta gerar o conteúdo com IA (hook/corpo/CTA mais persuasivos e
        únicos). Se a IA estiver desligada nas configurações, sem chave de
        API, ou a chamada falhar/vier em formato inesperado, cai de volta
        para os templates prontos em `generate()` — nunca trava o fluxo de
        agendamento automático.
        """
        if settings.AI_CONTENT_GENERATION_ENABLED:
            ai_content = cls.generate_with_ai(product, tone)
            if ai_content is not None:
                return ai_content

        return cls.generate(product, tone=tone)

    @classmethod
    def generate_with_ai(
        cls,
        product: dict,
        tone: str = "oferta",
    ) -> dict | None:
        """
        Gera hook, corpo, CTA e hashtags usando um modelo de linguagem via
        OpenRouter, seguindo regras de copywriting (evita aberturas
        genéricas, usa curiosidade/especificidade no hook, CTA imperativa
        com benefício claro). Retorna None em qualquer falha, para quem
        chamar cair de volta no template.
        """
        name = product.get("name", "Produto")
        price = product.get("price", 0)
        rating = product.get("rating", 0)
        sales = product.get("sales", 0)

        user_message = (
            f"Produto: {name}\n"
            f"Preço: R$ {price:.2f}\n"
            f"Avaliação: {rating:.1f} de 5\n"
            f"Vendas: {sales}\n"
            f"Tom desejado: {tone}\n"
            f"Gere o JSON conforme as instruções."
        )

        try:
            result = ai_agent_service.generate_reply(
                provider="openrouter",
                model_name=settings.OPENROUTER_MODEL,
                system_prompt=AI_SYSTEM_PROMPT,
                user_message=user_message,
            )
            if not result.get("ok"):
                cls.log_info(f"IA de conteúdo indisponível, usando template: {result.get('error')}")
                return None

            raw = result["reply"].strip()
            if raw.startswith("```"):
                raw = raw.strip("`")
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw
                if raw.lower().startswith("json"):
                    raw = raw.split("\n", 1)[1] if "\n" in raw else ""

            data = json.loads(raw)
            hook = str(data["hook"]).strip()
            body = str(data["body"]).strip()
            cta = str(data["cta"]).strip()
            hashtags_list = data["hashtags"]
            hashtags = " ".join(
                h if h.startswith("#") else f"#{h}" for h in hashtags_list
            )

            if not hook or not body or not cta or not hashtags_list:
                return None

            title = f"{hook}: {name}"
            caption = f"{hook}\n\n{body}\n\n{cta}"

            cls.log_success("Conteúdo gerado com IA (hook/CTA personalizados).")

            return {
                "title": title,
                "caption": caption,
                "hashtags": hashtags,
                "target_audience": cls._suggest_audience(product),
                "channel": cls._suggest_channel(product),
                "estimated_commission": product.get("commission", 0),
                "tone": tone,
                "ai_generated": True,
            }
        except Exception as exc:
            cls.log_info(f"Falha ao gerar conteúdo com IA, usando template: {exc}")
            return None

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
