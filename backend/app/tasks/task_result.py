"""
TrendZone AI OS
================================

TaskResult

Resultado padronizado retornado
por qualquer Task.
"""

from dataclasses import dataclass, field

from typing import Any


@dataclass
class TaskResult:

    success: bool

    task: str

    message: str

    data: Any = None

    errors: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def add_error(self, message: str):

        self.errors.append(message)

    def add_warning(self, message: str):

        self.warnings.append(message)

    def add_metadata(self, key: str, value):

        self.metadata[key] = value

    @property
    def failed(self):

        return not self.success