"""
TrendZone AI OS
================================

Model responsável pelas credenciais de Marketplace
de cada usuário (multi-tenant).

Cada usuário conecta a conta de afiliado dele por
marketplace. Os tokens são armazenados CRIPTOGRAFADOS
(ver services.marketplace_account_service).

Marketplaces suportados (core.enums.Marketplace):
- shopee
- mercado_livre
- amazon
- aliexpress
- magalu
- tiktok
"""

from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import BaseModel


class MarketplaceAccount(BaseModel):
    """
    Conta de marketplace conectada por um usuário.
    """

    __tablename__ = "marketplace_accounts"

    __table_args__ = (

        Index("idx_mkt_acc_user", "user_id"),

        Index("idx_mkt_acc_marketplace", "marketplace"),

        UniqueConstraint(
            "user_id",
            "marketplace",
            name="uq_mkt_acc_user_marketplace",
        ),

    )

    # =====================================================
    # Vínculo
    # =====================================================

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    marketplace: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # =====================================================
    # Credenciais (sempre criptografadas em repouso)
    # =====================================================

    access_token: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    refresh_token: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    extra: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    # =====================================================
    # Estado
    # =====================================================

    status: Mapped[str] = mapped_column(
        String(20),
        default="conectada",
    )

    last_validated_at: Mapped[str] = mapped_column(
        String(30),
        default="",
    )
