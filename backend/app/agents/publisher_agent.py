"""
TrendZone AI OS
================================

Publisher Agent

Última etapa do Pipeline.

Responsável por publicar os resultados do Pipeline:
- Salva produtos aprovados no banco de dados
- Gera campanhas de divulgação automáticas
- Registra logs de auditoria
- Notifica o usuário sobre novos produtos promovidos
"""

from app.agents.base_agent import BaseAgent
from app.agents.result import AgentResult
from app.core.logger import logger


class PublisherAgent(BaseAgent):

    AGENT_ID = "PUBLISHER"

    NAME = "Publisher Agent"

    VERSION = "3.0"

    DESCRIPTION = (
        "Responsável pela publicação "
        "dos resultados do Pipeline: "
        "persiste produtos, gera campanhas "
        "e notifica o usuário."
    )

    def execute(self, context):

        try:

            reports = context.get_reports()
            published = []
            errors = []

            for report in reports:

                decision = report.get("decision", "")
                if decision not in ("PROMOVER", "MONITORAR"):
                    continue

                try:
                    self._persist_product(report)
                    published.append(report)
                except Exception as e:
                    errors.append(str(e))

            if published:
                try:
                    self._notify_new_products(published)
                except Exception:
                    pass

            context.set_metadata(
                "published_reports",
                len(published),
            )

            context.set_metadata(
                "publish_errors",
                len(errors),
            )

            return AgentResult(
                success=True,
                agent=self.AGENT_ID,
                message=(
                    f"{len(published)} produto(s) publicado(s), "
                    f"{len(errors)} erro(s)."
                ),
                data=published,
            )

        except Exception as e:

            result = AgentResult(
                success=False,
                agent=self.AGENT_ID,
                message="Erro durante publicação.",
            )
            result.add_error(str(e))
            return result

    def _persist_product(self, report: dict):
        from app.database.session import SessionLocal
        from app.repositories.product_repository import ProductRepository
        from app.services.product_service import ProductService
        from app.schemas.product import ProductCreate

        node = report.get("node") or report
        item_id = node.get("itemId")
        if not item_id:
            return

        db = SessionLocal()
        try:
            existing = ProductRepository.get_by_item_id(db, item_id)
            if existing:
                if report.get("score"):
                    existing.score = report["score"]
                    db.commit()
                return

            ProductService.create(
                db,
                ProductCreate(
                    marketplace=node.get("marketplace", "shopee"),
                    item_id=item_id,
                    shop_id=node.get("shopId", 0),
                    category="geral",
                    name=node.get("productName", ""),
                    price=node.get("price", 0),
                    commission=float(node.get("commissionRate") or 0) * 100,
                    image=node.get("imageUrl", ""),
                    offer_link=node.get("offerLink", ""),
                    rating=float(node.get("ratingStar") or 0),
                    sales=int(node.get("sales") or 0),
                ),
            )
            db.commit()
            logger.info(
                f"[PUBLISHER] Produto {item_id} salvo no banco."
            )
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def _notify_new_products(self, published: list):
        from app.database.session import SessionLocal
        from app.services.notification_service import NotificationService

        db = SessionLocal()
        try:
            names = [
                p.get("node", p).get("productName", "?")[:30]
                for p in published[:5]
            ]
            extra = len(published) - len(names)
            msg = f"Auto-Scout encontrou {len(published)} produto(s): "
            msg += ", ".join(names)
            if extra > 0:
                msg += f" (+{extra} mais)"

            NotificationService.create(
                db,
                user_id=1,
                title="Novos Produtos Encontrados",
                message=msg,
            )
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()