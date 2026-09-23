"""
TrendZone AI OS — Auto Publisher Service

Auto-Divulgador: roda em segundo plano dentro do
proprio backend e, nos horarios configurados em
Schedule, gera automaticamente o conteudo de
divulgacao (via OpportunityEngine) dos melhores
produtos e salva como Campaign pronta para revisao.

Nao publica nem envia nada para terceiros —
apenas prepara o material automaticamente,
eliminando o clique manual de "gerar conteudo".
Quem decide publicar continua sendo o usuario,
na aba Oportunidades / Vendas & Comissoes.
"""

import asyncio
from datetime import datetime, date

from app.core.logger import logger
from app.database.session import SessionLocal
from app.repositories.product_repository import ProductRepository
from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.campaign_repository import CampaignRepository
from app.models.campaign import Campaign
from app.services.opportunity_engine import OpportunityEngine


CHECK_INTERVAL_SECONDS = 60


class AutoPublisherService:

    _task: asyncio.Task | None = None
    _running = False

    @classmethod
    def start(cls):
        if cls._running:
            return
        cls._running = True
        cls._task = asyncio.create_task(cls._loop())
        logger.info("[AUTO_PUBLISHER] Servico iniciado.")

    @classmethod
    def stop(cls):
        cls._running = False
        if cls._task:
            cls._task.cancel()
        logger.info("[AUTO_PUBLISHER] Servico parado.")

    @classmethod
    async def _loop(cls):
        while cls._running:
            try:
                cls._run_check()
            except Exception as e:
                logger.warning(f"[AUTO_PUBLISHER] Erro no ciclo: {e}")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)

    @classmethod
    def _run_check(cls):
        now = datetime.now()
        today = date.today().isoformat()
        current_hhmm = now.strftime("%H:%M")

        db = SessionLocal()
        try:
            schedules = ScheduleRepository.get_active(db)

            for sched in schedules:
                if sched.hora != current_hhmm:
                    continue
                if sched.ultimo_run == today:
                    continue

                cls._generate_campaigns(db, sched.quantos or 5)

                sched.ultimo_run = today
                sched.updated_at = datetime.utcnow()
                ScheduleRepository.update(db, sched)

                logger.info(
                    f"[AUTO_PUBLISHER] Execucao automatica concluida "
                    f"para agendamento '{sched.nicho}' ({sched.quantos} produto(s))."
                )
        finally:
            db.close()

    @classmethod
    def _generate_campaigns(cls, db, limit: int):
        products = ProductRepository.get_all(db)
        products_dict = [
            {
                "id": p.id, "item_id": p.item_id, "name": p.name,
                "image": p.image, "offer_link": p.offer_link,
                "price": float(p.price), "commission": float(p.commission),
                "rating": p.rating, "sales": p.sales,
                "score": p.score, "confidence": p.confidence,
                "recommendation": p.recommendation,
            }
            for p in products
        ]

        opportunities = OpportunityEngine.find(products_dict, limit=limit)

        for op in opportunities:
            product = op["product"]
            content = op["content"]

            existing = [
                c for c in CampaignRepository.get_all(db)
                if c.product_id == product["id"] and c.status == "DRAFT"
            ]
            if existing:
                continue

            campaign = Campaign(
                product_id=product["id"],
                title=content["title"],
                caption=content["caption"],
                hashtags=content["hashtags"],
                target_audience=content["target_audience"],
                channel=content["channel"],
                status="DRAFT",
            )
            CampaignRepository.create(db, campaign)
