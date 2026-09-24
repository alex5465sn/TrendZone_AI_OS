"""
TrendZone AI OS — Auto Scout Service

Roda em segundo plano dentro do backend e varre
periodicamente uma rotacao de palavras-chave reais
(mesmas categorias usadas na tela de Prospeccao),
alimentando a tabela "products" automaticamente.

Sem isso, a IA (Oportunidades, Descoberta, Funil,
Automacao) fica sempre vazia, pois depende de
produtos reais existirem no catalogo — e antes disso
o catalogo so crescia quando alguem clicava
manualmente em "Buscar" na tela de Prospeccao.
"""

import asyncio

from app.core.logger import logger
from app.database.session import SessionLocal
from app.services.scout_service import ScoutService
from app.constants.categories import get_keyword_rotation

CHECK_INTERVAL_SECONDS = 15 * 60

KEYWORD_ROTATION = get_keyword_rotation()


class AutoScoutService:

    _task: asyncio.Task | None = None
    _running = False
    _index = 0

    @classmethod
    def start(cls):
        if cls._running:
            return
        cls._running = True
        cls._task = asyncio.create_task(cls._loop())
        logger.info("[AUTO_SCOUT] Servico iniciado.")

    @classmethod
    def stop(cls):
        cls._running = False
        if cls._task:
            cls._task.cancel()
        logger.info("[AUTO_SCOUT] Servico parado.")

    @classmethod
    async def _loop(cls):
        while cls._running:
            try:
                cls._run_once()
            except Exception as e:
                logger.warning(f"[AUTO_SCOUT] Erro no ciclo: {e}")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)

    @classmethod
    def _run_once(cls):
        category_id, keyword = KEYWORD_ROTATION[cls._index % len(KEYWORD_ROTATION)]
        cls._index += 1

        db = SessionLocal()
        try:
            reports = ScoutService(db).search_products(keyword=keyword, page=1, limit=10)
            db.commit()
            logger.info(
                f"[AUTO_SCOUT] Categoria '{category_id}' / palavra-chave '{keyword}': "
                f"{len(reports)} produto(s) processado(s)."
            )
        except Exception as e:
            db.rollback()
            logger.warning(f"[AUTO_SCOUT] Falha ao varrer '{keyword}': {e}")
        finally:
            db.close()
