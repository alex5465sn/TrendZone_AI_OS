"""
TrendZone AI OS — Prospect Engine

Inspirado na Máquina de Leads: analisa os produtos
cadastrados, agrupa por nicho/categoria, calcula um
score de oportunidade e classifica como
quente / morno / frio.

Gera um dossiê com estatísticas do nicho e
sugestão de abordagem + canal de divulgação.
"""

import json
from typing import List

from app.services.base_service import BaseService


class ProspectEngine(BaseService):

    SERVICE_NAME = "PROSPECT_ENGINE"

    _CANAIS = {
        "quente": "Grupo de ofertas no WhatsApp",
        "morno": "Canal de cupons no Telegram",
        "frio": "Comunidade de achadinhos no Facebook",
    }

    _ABORDAGENS = {
        "quente": (
            "Nicho em alta! Publique imediatamente nos seus "
            "canais principais com o link de afiliado. "
            "Foque no preço baixo e alta avaliação."
        ),
        "morno": (
            "Nicho com potencial. Teste publicações em "
            "grupos menores e monitore cliques antes de "
            "escalar para canais maiores."
        ),
        "frio": (
            "Nicho com pouco volume. Acompanhe a evolução "
            "dos preços e vendas antes de investir energia "
            "em divulgação."
        ),
    }

    @classmethod
    def prospect(
        cls,
        products: List[dict],
        nicho: str = "",
    ) -> List[dict]:

        cls.log_info("Prospectando nichos de oportunidade...")

        grupos = cls._agrupar_por_nicho(products, nicho)

        prospects = []

        for nome_nicho, itens in grupos.items():

            score = cls._calcular_score(itens)

            temperatura = cls._temperatura(score)

            preco_medio = (
                sum(p.get("price", 0) for p in itens) / len(itens)
                if itens else 0
            )
            comissao_media = (
                sum(p.get("commission", 0) for p in itens) / len(itens)
                if itens else 0
            )
            vendas_total = sum(p.get("sales", 0) for p in itens)

            dossie = {
                "nicho": nome_nicho,
                "qtd_produtos": len(itens),
                "preco_medio": round(preco_medio, 2),
                "comissao_media": round(comissao_media, 2),
                "vendas_total": vendas_total,
                "score_medio_produtos": round(
                    sum(p.get("score", 0) for p in itens) / len(itens), 1
                ) if itens else 0,
                "melhor_produto": (
                    max(itens, key=lambda p: p.get("score", 0)).get("name", "")
                    if itens else ""
                ),
            }

            prospects.append({
                "nicho": nome_nicho,
                "cidade": "",
                "busca": nicho or "todos",
                "nome": f"Nicho: {nome_nicho}",
                "score": score,
                "temperatura": temperatura,
                "abordagem": cls._ABORDAGENS[temperatura],
                "dossie": json.dumps(dossie, ensure_ascii=False),
                "canal_sugerido": cls._CANAIS[temperatura],
                "status": "novo",
                "produto_ids": ",".join(
                    str(p.get("id", "")) for p in itens
                ),
                "qtd_produtos": len(itens),
                "preco_medio": round(preco_medio, 2),
                "comissao_media": round(comissao_media, 2),
                "vendas_total": vendas_total,
            })

        prospects.sort(key=lambda p: p["score"], reverse=True)

        cls.log_success(
            f"{len(prospects)} nicho(s) prospectado(s)."
        )

        return prospects

    @classmethod
    def _agrupar_por_nicho(
        cls,
        products: List[dict],
        filtro: str = "",
    ) -> dict:

        grupos: dict[str, list] = {}

        for p in products:
            nome = p.get("name", "")
            nicho = cls._extrair_nicho(nome)

            if filtro and filtro.lower() not in nicho.lower():
                continue

            grupos.setdefault(nicho, []).append(p)

        return grupos

    @classmethod
    def _extrair_nicho(cls, nome: str) -> str:
        palavras = nome.split()
        if len(palavras) >= 2:
            return " ".join(palavras[:2]).title()
        return nome.title() or "Geral"

    @classmethod
    def _calcular_score(cls, itens: List[dict]) -> int:
        if not itens:
            return 0

        score_medio = sum(p.get("score", 0) for p in itens) / len(itens)
        volume = min(30, len(itens) * 6)
        vendas = min(25, sum(p.get("sales", 0) for p in itens) // 10)
        comissao = min(20, int(
            sum(p.get("commission", 0) for p in itens)
            / len(itens) * 100
        ))
        rating = min(25, int(
            sum(p.get("rating", 0) for p in itens)
            / len(itens) * 5
        ))

        total = int(score_medio * 0.3 + volume + vendas + comissao + rating)
        return max(0, min(100, total))

    @classmethod
    def _temperatura(cls, score: int) -> str:
        if score >= 70:
            return "quente"
        if score >= 45:
            return "morno"
        return "frio"
