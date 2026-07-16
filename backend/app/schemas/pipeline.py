"""
TrendZone AI OS
===============================

Schemas utilizados pelo Pipeline
de Inteligência Artificial.
"""

from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)


class PipelineResult(BaseModel):
    """
    Resultado de uma etapa do Pipeline.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    success: bool

    stage: str

    message: str

    data: Any | None = None