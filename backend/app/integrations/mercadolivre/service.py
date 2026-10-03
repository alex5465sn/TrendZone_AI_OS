"""
TrendZone AI OS
================================

Mercado Livre Service

Camada de alto nível responsável por
consumir a API oficial do Mercado Livre.

Normaliza os resultados do catálogo do
Mercado Livre para o MESMO formato de
"nodes" já utilizado pela busca da Shopee
(``productOfferV2``), permitindo que todo o
restante do sistema (score, decisão da IA,
auto-add, promote, divulgação) funcione
sem nenhuma alteração por marketplace.

Diferenças importantes vs. Shopee:

- IDs do ML são strings ("MLB1234567890").
  Internamente o TrendZone usa item_id
  numérico: "MLB1234567890" -> 1234567890.
  O link completo (permalink) já guarda o
  identificador original.

- A API do ML não informa a comissão de
  afiliado por produto (o programa ML
  Afiliados não expõe API). Usamos uma
  comissão estimada configurável
  (MERCADOLIVRE_DEFAULT_COMMISSION), que
  pode ser ajustada por produto.
"""

from __future__ import annotations

import re
from typing import Any

from app.core.settings import settings
from app.integrations.mercadolivre.client import (
    MercadoLivreClient,
    MercadoLivreException,
)

ML_ITEM_ID_PATTERN = re.compile(
    r"^(?:MLB|[A-Z]{2}[A-Z0-9]?)\-?(\d{4,})$",
    re.IGNORECASE,
)

MARKETPLACE_NAME = "mercado_livre"


class MercadoLivreService:

    def __init__(
        self,
        client: MercadoLivreClient | None = None,
    ) -> None:

        self.client = client or MercadoLivreClient()

    # =====================================================
    # IDs
    # =====================================================

    @staticmethod
    def external_id_to_int(
        external_id: str,
    ) -> int | None:
        """
        "MLB1234567890" -> 1234567890

        Retorna None quando o ID não puder ser
        representado como inteiro (formato novo
        de ID não numérico), e nesse caso o item
        é ignorado pela importação.
        """

        if external_id is None:

            return None

        match = ML_ITEM_ID_PATTERN.match(
            str(external_id).strip(),
        )

        if match:

            return int(match.group(1))

        # Alguns endpoints devolvem apenas o número.

        if str(external_id).isdigit():

            return int(external_id)

        return None

    @staticmethod
    def int_to_external_id(
        item_id: int,
    ) -> str:
        """
        1234567890 -> "MLB1234567890"
        """

        return f"MLB{int(item_id)}"

    # =====================================================
    # Search (formato compatível com a Shopee)
    # =====================================================

    def search_products(
        self,
        keyword: str = "",
        page: int = 1,
        limit: int = 20,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Busca produtos no catálogo do Mercado Livre
        e devolve no mesmo formato da busca da Shopee:

        {
            "nodes": [ ... ],
            "pageInfo": {
                "page": 1,
                "limit": 20,
                "hasNextPage": true,
                "scrollId": ""
            }
        }

        Cada node contém os campos que o restante do
        sistema já conhece: itemId, shopId, productName,
        imageUrl, offerLink, price, commissionRate,
        ratingStar, sales, marketplace...
        """

        keyword = (keyword or "").strip() or "ofertas"

        page = max(1, int(page or 1))
        limit = max(1, min(50, int(limit or 20)))

        offset = (page - 1) * limit

        raw = self.client.search_site(
            q=keyword,
            offset=offset,
            limit=limit,
        )

        paging = raw.get("paging") or {}

        nodes = []

        for result in raw.get("results") or []:

            node = self._to_node(result)

            if node is not None:

                nodes.append(node)

        total = int(paging.get("total") or 0)

        return {
            "nodes": nodes,
            "pageInfo": {
                "page": page,
                "limit": limit,
                "hasNextPage": bool(
                    offset + limit < total,
                ),
                "scrollId": "",
            },
        }

    # =====================================================
    # Item
    # =====================================================

    def get_item(
        self,
        external_id: str,
    ) -> dict[str, Any]:
        """
        Detalhe público de um item do ML
        ("MLB1234567890"), normalizado.
        """

        raw = self.client.get_item(
            external_id,
        )

        return self._to_node(raw) or {}

    # =====================================================
    # Normalização
    # =====================================================

    def _to_node(
        self,
        result: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Converte um resultado bruto do ML no
        formato de node compatível com a Shopee.
        """

        if not result:
            return None

        external_id = str(
            result.get("id") or "",
        ).strip()

        item_id = self.external_id_to_int(
            external_id,
        )

        if item_id is None:
            # Formato de ID desconhecido — não importa.
            return None

        seller = result.get("seller") or {}

        shop_id = 0

        try:

            shop_id = int(seller.get("id") or 0)

        except (TypeError, ValueError):

            shop_id = 0

        price = self._price(result)

        commission = float(
            settings.MERCADOLIVRE_DEFAULT_COMMISSION,
        )

        rating = self._rating(result)

        sales = int(
            result.get("sold_quantity") or 0,
        )

        if sales < 0:
            # API recente devolve -1 quando indisponível.
            sales = 0

        permalink = str(
            result.get("permalink") or "",
        )

        image = self._image(result)

        return {
            # Campos no formato Shopee (compatibilidade total)
            "itemId": item_id,
            "externalId": external_id,
            "marketplace": MARKETPLACE_NAME,
            "shopId": shop_id,
            "shopName": str(
                seller.get("nickname")
                or "",
            ),
            "productName": str(
                result.get("title") or "",
            ),
            "productLink": permalink,
            "offerLink": permalink,
            "imageUrl": image,
            "price": price,
            "priceMin": price,
            "priceMax": price,
            "sales": sales,
            "commission": f"{commission:.2f}",
            "commissionRate": f"{commission / 100:.4f}",
            "ratingStar": f"{rating:.1f}",
            "priceDiscountRate": 0,
            "productCatIds": [],
            "category": str(
                result.get("domain_id")
                or "",
            ),
            # ML não possui frete grátis explícito no
            # mesmo formato; shipping free é booleano.
            "freeShipping": bool(
                (result.get("shipping") or {}).get("free_shipping"),
            ),
            "originalPrice": self._original_price(result),
        }

    @staticmethod
    def _price(
        result: dict[str, Any],
    ) -> str:
        """
        Preço atual como string (compatível com a Shopee,
        que devolve string no campo price).
        """

        price = result.get("price")

        try:

            return f"{float(price):.2f}"

        except (TypeError, ValueError):

            return "0.00"

    @staticmethod
    def _original_price(
        result: dict[str, Any],
    ) -> float:
        """
        Preço original (sem desconto), quando existir.
        """

        try:

            return float(
                result.get("original_price")
                or result.get("price")
                or 0,
            )

        except (TypeError, ValueError):

            return 0.0

    @staticmethod
    def _rating(
        result: dict[str, Any],
    ) -> float:
        """
        Média de avaliação (0-5). A API do ML
        devolve em ``reviews.rating_average``.
        """

        reviews = result.get("reviews") or {}

        try:

            rating = float(
                reviews.get("rating_average") or 0,
            )

        except (TypeError, ValueError):

            rating = 0.0

        return max(0.0, min(5.0, rating))

    @staticmethod
    def _image(
        result: dict[str, Any],
    ) -> str:
        """
        Imagem em resolução maior.

        O ML devolve thumbnail no sufixo -I (baixa
        resolução). Trocamos para -O (original/alta).
        """

        pictures = result.get("pictures") or []

        if pictures and pictures[0].get("url"):

            return str(pictures[0]["url"])

        thumbnail = str(
            result.get("thumbnail") or "",
        )

        if thumbnail.endswith("-I.jpg"):

            return thumbnail[:-6] + "-O.jpg"

        return thumbnail
