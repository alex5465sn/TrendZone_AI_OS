"""
TrendZone AI OS
================================

TaskContext

Objeto compartilhado entre todas
as Tasks do Pipeline.

Responsável por armazenar:

- Dados
- Metadados
- Histórico
- Configurações
- Resultados
"""

from typing import Any


class TaskContext:

    def __init__(self):

        self._data: dict[str, Any] = {}

        self._metadata: dict[str, Any] = {}

        self._history: list[str] = []

    # ==========================
    # DATA
    # ==========================

    def set(self, key: str, value: Any):

        self._data[key] = value

    def get(self, key: str, default=None):

        return self._data.get(key, default)

    def has(self, key: str) -> bool:

        return key in self._data

    def remove(self, key: str):

        self._data.pop(key, None)

    def data(self):

        return self._data

    # ==========================
    # METADATA
    # ==========================

    def set_metadata(self, key: str, value: Any):

        self._metadata[key] = value

    def get_metadata(self, key: str, default=None):

        return self._metadata.get(key, default)

    def metadata(self):

        return self._metadata

    # ==========================
    # HISTORY
    # ==========================

    def add_history(self, message: str):

        self._history.append(message)

    def history(self):

        return self._history

    # ==========================
    # RESET
    # ==========================

    def clear(self):

        self._data.clear()

        self._metadata.clear()

        self._history.clear()