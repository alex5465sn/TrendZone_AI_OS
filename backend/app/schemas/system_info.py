"""
TrendZone AI OS
===============================

Schemas responsáveis pelas informações
institucionais do sistema.
"""

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


class SystemInfoBase(BaseModel):

    app_name: str

    version: str


# =====================================================
# CREATE
# =====================================================

class SystemInfoCreate(SystemInfoBase):
    """
    Cadastro das informações
    da instalação.
    """

    pass


# =====================================================
# RESPONSE
# =====================================================

class SystemInfoResponse(SystemInfoBase):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    uuid: str

    status: str

    environment: str

    is_active: bool

    created_at: datetime

    updated_at: datetime