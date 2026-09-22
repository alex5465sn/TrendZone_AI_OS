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
from app.integrations.facebook.facebook_client import FacebookClient
from app.services.facebook_auto_post_service import run_daily_auto_schedule

CHECK_INTERVAL_SECONDS = 60
AUTO_SCHEDULE_INTERVAL_CYCLES = 60


class FacebookSchedulerService:

    _task: asyncio.Task | None = None
    _running = False

    @classmethod
    def start(cls):
        if cls._running:
            return
        cls._running = True
        cls._task = asyncio.create_task(cls._loop())
        try:
            run_daily_auto_schedule()
        except Exception as e:
            logger.warning(f"[FB_SCHEDULER] Erro no agendamento automatico inicial: {e}")
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
                if cycle % AUTO_SCHEDULE_INTERVAL_CYCLES == 0:
                    run_daily_auto_schedule()
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
                except Exception as e:
                    post.status = "erro"
                    post.error_message = str(e)[:500]
                    logger.warning(f"[FB_SCHEDULER] Falha ao publicar post agendado #{post.id}: {e}")

                ScheduledPostRepository.update(db, post)
        finally:
            db.close()
