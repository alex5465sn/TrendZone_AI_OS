"""
TrendZone AI OS
================================

Base Checker

Classe base para todos os
Checkers do Enterprise Audit.
"""

from abc import ABC
from abc import abstractmethod

from tools.report import AuditReport


class BaseChecker(ABC):
    """
    Classe base para todos os
    verificadores do sistema.
    """

    NAME = "Unnamed Checker"

    DESCRIPTION = ""

    @classmethod
    @abstractmethod
    def run(
        cls,
        report: AuditReport,
    ) -> None:
        """
        Executa o checker.
        """
        raise NotImplementedError