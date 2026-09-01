"""
TrendZone AI OS
================================

Audit Report

Responsável por armazenar e gerar
o relatório final da auditoria.
"""

from dataclasses import dataclass, field


@dataclass
class AuditItem:

    module: str

    success: bool

    message: str

    warnings: list[str] = field(default_factory=list)


class AuditReport:

    def __init__(self):

        self.items: list[AuditItem] = []

    def add(

        self,

        module: str,

        success: bool,

        message: str,

        warnings=None,

    ):

        self.items.append(

            AuditItem(

                module=module,

                success=success,

                message=message,

                warnings=warnings or [],

            )

        )

    def score(self):

        if not self.items:

            return 0

        passed = sum(

            item.success

            for item in self.items

        )

        return round(

            (passed / len(self.items)) * 100,

            2,

        )

    def warnings(self):

        warnings = []

        for item in self.items:

            warnings.extend(item.warnings)

        return warnings