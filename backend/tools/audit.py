"""
TrendZone AI OS
Enterprise Audit Engine
"""

from tools.core.loader import CheckerLoader
from tools.core.report import AuditReport


class EnterpriseAudit:

    def __init__(self):

        self.registry = CheckerLoader.build()

    def execute(self) -> AuditReport:

        report = AuditReport()

        for checker in self.registry.items:

            checker.run(report)

        return report