"""
TrendZone AI OS — Facebook Scheduler Service

Roda em segundo plano dentro do backend e, quando chega a
data/hora agendada, publica automaticamente o post (texto/imagem
ou vídeo) na página do Facebook.
"""

import asyncio
from datetime import datetime

from app.core.logger import logger
from app.database.session import SessionLocal
from app.repositories.scheduled_post_repository import ScheduledPostRepository
from app.repositories.product_repository import ProductRepository
from app.integrations.facebook.facebook_client import FacebookClient
from app.services.facebook_auto_post_service import run_daily_auto_schedule
from app.services.product_performance_score import run_performance_recalculation
from app.services.sales_tracker_service import run_sales_sync
from app.services.notification_service import send_push_notification

CHECK_INTERVAL_SECONDS = 60
AUTO_SCHEDULE_INTERVAL_CYCLES = 60
SALES_SYNC_INTERVAL_CYCLES = 30


class FacebookSchedulerService:

    _task: asyncio.Task | None = None
    _running = False

    # Observabilidade dos jobs de fundo: sem isso, um job que para de
    # ser chamado (como aconteceu com a sincronizacao de vendas) fica
    # invisivel ate alguem notar na "unha" que os dados pararam de
    # aparecer. Com isso da pra expor "ultima execucao" de cada job.
    _job_status: dict[str, dict] = {
        "sales_sync": {"last_run_at": None, "last_error": None},
        "daily_auto_schedule": {"last_run_at": None, "last_error": None},
        "performance_recalculation": {"last_run_at": None, "last_error": None},
    }

    @classmethod
    def _run_job(cls, name: str, fn) -> None:
        try:
            fn()
            cls._job_status[name] = {
                "last_run_at": datetime.utcnow().isoformat(),
                "last_error": None,
            }
        except Exception as e:
            logger.warning(f"[FB_SCHEDULER] Erro no job '{name}': {e}")
            cls._job_status[name] = {
                "last_run_at": datetime.utcnow().isoformat(),
                "last_error": str(e)[:300],
            }

    @classmethod
    def get_health(cls) -> dict:
        """
        Status da ultima execucao de cada job de fundo, para
        detectar silenciosamente um job que parou de rodar
        (sem precisar esperar o usuario notar na pratica).
        """
        now = datetime.utcnow()
        health = {}
        for name, status in cls._job_status.items():
            last_run_at = status.get("last_run_at")
            seconds_since = None
            if last_run_at:
                seconds_since = (now - datetime.fromisoformat(last_run_at)).total_seconds()
            health[name] = {
                "last_run_at": last_run_at,
                "seconds_since_last_run": seconds_since,
                "last_error": status.get("last_error"),
                "never_ran": last_run_at is None,
            }
        health["scheduler_running"] = cls._running
        return health

    @classmethod
    def start(cls):
        if cls._running:
            return
        cls._running = True
        cls._task = asyncio.create_task(cls._loop())
        cls._run_job("daily_auto_schedule", run_daily_auto_schedule)
        cls._run_job("sales_sync", run_sales_sync)
        cls._run_job("performance_recalculation", run_performance_recalculation)
        logger.info("[FB_SCHEDULER] Servico iniciado.")

    @classmethod
    def stop(cls):
        cls._running = False
        if cls._task:
            cls._task.cancel()
        logger.info("[FB_SCHEDULER] Servico parado.")

    @classmethod
    async def _loop(cls):
        cycle = 0
        while cls._running:
            try:
                cls._run_check()
                cycle += 1
                if cycle % SALES_SYNC_INTERVAL_CYCLES == 0:
                    cls._run_job("sales_sync", run_sales_sync)
                if cycle % AUTO_SCHEDULE_INTERVAL_CYCLES == 0:
                    cls._run_job("daily_auto_schedule", run_daily_auto_schedule)
                    cls._run_job("performance_recalculation", run_performance_recalculation)
            except Exception as e:
                logger.warning(f"[FB_SCHEDULER] Erro no ciclo: {e}")
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)

    @classmethod
    def _run_check(cls):
        db = SessionLocal()
        try:
            due_posts = ScheduledPostRepository.get_due(db, datetime.utcnow())
            if not due_posts:
                return

            client = FacebookClient()

            for post in due_posts:
                try:
                    if post.video_path:
                        client.publish_video(post.video_path, description=post.message)
                    else:
                        client.publish_post(
                            message=post.message,
                            link=post.link or None,
                            image_url=post.image_url or None,
                        )
                    post.status = "publicado"
                    post.error_message = ""
                    logger.info(f"[FB_SCHEDULER] Post agendado #{post.id} publicado com sucesso.")

                    product = ProductRepository.get_by_item_id(db, post.product_item_id)
                    nome_produto = product.name if product else f"produto #{post.product_item_id}"
                    send_push_notification(
                        title="✅ Post publicado no Facebook",
                        message=f"{nome_produto} foi publicado com sucesso na sua pagina.",
                    )
                except Exception as e:
                    post.status = "erro"
                    post.error_message = str(e)[:500]
                    logger.warning(f"[FB_SCHEDULER] Falha ao publicar post agendado #{post.id}: {e}")
                    send_push_notification(
                        title="❌ Falha ao publicar post",
                        message=f"Post #{post.id} nao pode ser publicado: {str(e)[:150]}",
                        tags="warning",
                    )

                ScheduledPostRepository.update(db, post)
        finally:
            db.close()
