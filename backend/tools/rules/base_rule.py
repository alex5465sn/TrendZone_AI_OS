"""
TrendZone AI OS
Enterprise Audit

Base Rule
"""

from abc import ABC, abstractmethod

from tools.core.finding import Finding


class BaseRule(ABC):
    """
    Classe base para todas as regras.
    """

    ID = ""

    TITLE = ""

    DESCRIPTION = ""

    @abstractmethod
    def execute(self, file, tree) -> list[Finding]:
        """
        Executa a regra.

        Retorna uma lista de Findings.
        """
        raise NotImplementedError