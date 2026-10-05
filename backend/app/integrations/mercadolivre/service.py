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
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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

        # O endpoint de busca livre ("/sites/{site}/search") é
        # bloqueado pelo Mercado Livre para apps não certificados
        # (403 "forbidden"). Em seu lugar, usamos "/products/search"
        # (ficha de catálogo por palavra-chave), que continua
        # disponível.
        #
        # Nem todo produto de catálogo tem oferta ativa no momento
        # ("/products/{id}/items" devolve 404 "No winners found"
        # para quem não tem vendedor no momento) — na prática só
        # uma fração dos resultados de catálogo tem preço. Por
        # isso varremos um lote maior de candidatos por página
        # (RAW_BATCH_SIZE), em paralelo, até reunir "limit"
        # produtos com oferta válida.
        raw_window_start = (page - 1) * self.RAW_SCAN_PER_PAGE

        nodes: list[dict[str, Any]] = []
        raw_scanned = 0
        total = 0
        started_at = time.monotonic()

        while (
            len(nodes) < limit
            and raw_scanned < self.RAW_SCAN_PER_PAGE
            # Palavras-chave com pouca oferta ativa podem exigir
            # vários lotes — nesse caso é melhor devolver menos
            # resultados rápido do que travar a busca do usuário.
            and (time.monotonic() - started_at) < self.MAX_SEARCH_SECONDS
        ):

            batch_offset = raw_window_start + raw_scanned

            # "/products/search" só permite acessar os primeiros
            # ~150 resultados de cada busca (offset máximo 100,
            # mesmo quando "paging.total" informa um valor bem
            # maior) — passar disso devolve 400 "Invalid arguments".
            if batch_offset > self.MAX_RAW_OFFSET:
                break

            batch_size = min(
                self.RAW_BATCH_SIZE,
                self.RAW_SCAN_PER_PAGE - raw_scanned,
                self.MAX_RAW_OFFSET + self.RAW_BATCH_SIZE - batch_offset,
            )

            if batch_size <= 0:
                break

            raw = self.client.products_search(
                q=keyword,
                offset=batch_offset,
                limit=batch_size,
            )

            paging = raw.get("paging") or {}
            total = int(paging.get("total") or 0)

            results = raw.get("results") or []

            if not results:
                break

            raw_scanned += len(results)

            nodes.extend(
                self._fetch_nodes(results, limit - len(nodes)),
            )

        # O catálogo só expõe os primeiros ~150 resultados por
        # palavra-chave, então o total "real" navegável é sempre
        # o menor entre o total informado pela API e esse limite.
        reachable_total = min(total, self.RAW_SCAN_PER_PAGE)

        return {
            "nodes": nodes[:limit],
            "pageInfo": {
                "page": page,
                "limit": limit,
                "hasNextPage": bool(
                    raw_window_start + raw_scanned < reachable_total,
                ),
                "scrollId": "",
            },
        }

    # Offset máximo aceito por "/products/search" — a API
    # devolve 400 "Invalid arguments" acima disso.
    MAX_RAW_OFFSET = 100

    # Tempo máximo (segundos) varrendo lotes extras em busca de
    # ofertas ativas, antes de devolver o que já foi encontrado.
    MAX_SEARCH_SECONDS = 9

    # Máximo de candidatos de catálogo varridos por página
    # (em lotes de RAW_BATCH_SIZE, em paralelo) até desistir.
    RAW_SCAN_PER_PAGE = 100

    # Tamanho máximo aceito por chamada a "/products/search".
    RAW_BATCH_SIZE = 50

    # Chamadas simultâneas a "/products/{id}/items".
    MAX_WORKERS = 15

    def _fetch_nodes(
        self,
        results: list[dict[str, Any]],
        wanted: int,
    ) -> list[dict[str, Any]]:
        """
        Para cada produto de catálogo em ``results``, busca a
        oferta vencedora em paralelo e monta o node (formato
        Shopee). Produtos sem oferta ativa são descartados.
        """

        by_id = {
            str(result.get("id") or "").strip(): result
            for result in results
            if result.get("id")
        }

        if not by_id:
            return []

        nodes: list[dict[str, Any]] = []

        with ThreadPoolExecutor(
            max_workers=self.MAX_WORKERS,
        ) as executor:

            futures = {
                executor.submit(
                    self.client.get_product_items,
                    product_id,
                ): product_id
                for product_id in by_id
            }

            for future in as_completed(futures):

                product_id = futures[future]

                try:

                    offers = future.result()

                except MercadoLivreException:
                    # Um produto específico instável não deve
                    # derrubar a página inteira de resultados.
                    continue

                if not offers:
                    continue

                best_offer = offers[0]
                result = by_id[product_id]

                merged = {
                    "id": product_id,
                    "title": result.get("name") or "",
                    "permalink": (
                        "https://www.mercadolivre.com.br/p/"
                        f"{product_id}"
                    ),
                    "pictures": result.get("pictures") or [],
                    "domain_id": result.get("domain_id") or "",
                    "seller": {"id": best_offer.get("seller_id")},
                    "price": best_offer.get("price"),
                    "original_price": best_offer.get(
                        "original_price",
                    ),
                    "shipping": best_offer.get("shipping") or {},
                    "sold_quantity": 0,
                    "reviews": {},
                }

                node = self._to_node(merged)

                if node is not None:
                    nodes.append(node)

        return nodes

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
