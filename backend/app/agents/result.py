"""
TrendZone AI OS
================================

Agent Result.

Objeto padrão retornado por todos
os Agents do sistema.

Nunca retorne listas ou dicionários
diretamente.
"""

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime
from typing import Any


@dataclass(slots=True)
class AgentResult:

    success: bool

    agent: str

    message: str = ""

    data: Any = None

    errors: list[str] = field(default_factory=list)

    started_at: datetime | None = None

    finished_at: datetime | None = None

    execution_time: float = 0.0

    metadata: dict = field(default_factory=dict)

    # ==============================================
    # HELPERS
    # ==============================================

    @property
    def has_errors(self):

        return len(self.errors) > 0

    def add_error(self, error: str):

        self.errors.append(error)

        self.success = False

    def set_metadata(self, key, value):

        self.metadata[key] = value

    def get_metadata(self, key):

        return self.metadata.get(key)

    def to_dict(self):

        return {

            "success": self.success,

            "agent": self.agent,

            "message": self.message,

            "data": self.data,

            "errors": self.errors,

            "execution_time": self.execution_time,

            "metadata": self.metadata,

        }