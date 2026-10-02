"""
TrendZone AI OS — Facebook Auto Post Service

Roda uma vez por dia: escolhe os melhores produtos rastreados
(por score), gera o conteúdo automaticamente e agenda a
publicação nos horários de pico definidos, sem intervenção manual.
O FacebookSchedulerService (já existente) publica quando chega a hora.
"""

import random
from datetime import datetime, timedelta

from app.core.logger import logger
from app.database.session import SessionLocal
from app.repositories.product_repository import ProductRepository
from app.repositories.scheduled_post_repository import ScheduledPostRepository
from app.models.scheduled_post import ScheduledPost
from app.services.content_generator_service import ContentGeneratorService
from app.services.image_generator_service import generate_cover_image
from app.services.notification_service import NotificationService
from app.services.sales_tracker_service import SalesTrackerService

PEAK_HOURS = [7, 9, 12, 16, 19]
PRODUCTS_PER_DAY = len(PEAK_HOURS)

# Rotação de tom dos posts automáticos: ~70% venda direta (oferta/urgencia),
# ~30% educativo/storytelling — pra não parecer só propaganda o dia todo.
TONE_WEIGHTS = {
    "oferta": 45,
    "urgencia": 25,
    "educativo": 20,
    "storytelling": 10,
}


def _build_tracking_link(product) -> str:
    """
    Gera um link curto da Shopee com subId = item_id do produto.

    Esse subId e o que a Shopee devolve como "utmContent" no
    ConversionReport, permitindo casar uma venda real com o
    produto que a gerou (sem isso o Score nunca aprende com
    vendas reais, so com cliques do proprio TrendZone).

    Se a geracao falhar, cai no link de oferta padrao (comportamento
    anterior) para nao travar o agendamento do post.
    """
    try:
        result = SalesTrackerService.generate_tracking_link(
            origin_url=product.offer_link,
            sub_ids=[str(product.item_id)],
        )
        if result.get("short_link"):
            return result["short_link"]
    except Exception as e:
        logger.warning(f"[FB_AUTO_POST] Erro ao gerar link rastreavel: {e}")

    return product.offer_link or ""


def _pick_tone() -> str:
    return random.choices(
        population=list(TONE_WEIGHTS.keys()),
        weights=list(TONE_WEIGHTS.values()),
        k=1,
    )[0]


def run_daily_auto_schedule() -> int:
    db = SessionLocal()
    created = 0
    try:
        today = datetime.utcnow().date()
        already_today = [
            p for p in ScheduledPostRepository.get_all_ordered(db)
            if p.scheduled_at.date() == today
        ]
        if already_today:
            logger.info("[FB_AUTO_POST] Ja existem posts agendados para hoje, pulando.")
            return 0

        recently_used = ScheduledPostRepository.get_recently_used_product_ids(db, days=30)
        products = ProductRepository.get_top_score(
            db, limit=PRODUCTS_PER_DAY, exclude_item_ids=recently_used,
        )

        if len(products) < PRODUCTS_PER_DAY:
            faltam = PRODUCTS_PER_DAY - len(products)
            ja_escolhidos = {p.item_id for p in products}
            complemento = ProductRepository.get_top_score(db, limit=faltam + len(recently_used))
            for produto in complemento:
                if produto.item_id not in ja_escolhidos:
                    products.append(produto)
                    ja_escolhidos.add(produto.item_id)
                if len(products) >= PRODUCTS_PER_DAY:
                    break

        if not products:
            logger.info("[FB_AUTO_POST] Nenhum produto rastreado para gerar posts.")
            return 0

        for product, hour in zip(products, PEAK_HOURS):
            content = ContentGeneratorService.generate_smart(
                {
                    "name": product.name,
                    "price": product.price,
                    "commission": product.commission,
                    "rating": product.rating,
                    "sales": product.sales,
                },
                tone=_pick_tone(),
            )
            scheduled_at = datetime.combine(today, datetime.min.time()) + timedelta(hours=hour)
            if scheduled_at < datetime.utcnow():
                scheduled_at += timedelta(days=1)

            try:
                cover_image = generate_cover_image(product.name)
            except Exception as e:
                logger.warning(f"[FB_AUTO_POST] Erro ao gerar imagem de capa com IA: {e}")
                cover_image = None
            image_url = cover_image or product.image or ""

            post = ScheduledPost(
                product_item_id=product.item_id,
                message=f"{content['caption']}\n\n{content['hashtags']}",
                link=_build_tracking_link(product),
                image_url=image_url,
                scheduled_at=scheduled_at,
                status="pendente",
            )
            ScheduledPostRepository.create(db, post)
            created += 1

            # Envia notificação ao usuário
            try:
                NotificationService.send_post_published_notification(
                    db,
                    user_id=1,  # TODO: obter user_id do contexto
                    product_name=product.name,
                    channel="facebook",
                    post_id=post.id,
                )
            except Exception as e:
                logger.warning(f"[FB_AUTO_POST] Erro ao enviar notificação: {e}")

        logger.info(f"[FB_AUTO_POST] {created} post(s) agendado(s) automaticamente para hoje.")
        return created
    except Exception as e:
        logger.warning(f"[FB_AUTO_POST] Erro ao gerar agendamento automatico: {e}")
        return created
    finally:
        db.close()
