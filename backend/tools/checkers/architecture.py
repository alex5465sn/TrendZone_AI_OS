from pathlib import Path

from tools.core.checker import Checker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class ArchitectureChecker(Checker):

    NAME = "Architecture"

    DESCRIPTION = "Arquitetura do Projeto"

    VERSION = "1.0"

    REQUIRED_DIRS = [

        "api",

        "models",

        "repositories",

        "services",

        "schemas",

        "agents",

        "tasks",

        "security",

    ]

    def run(
        self,
        report: AuditReport,
    ):

        app = Path("app")

        for folder in self.REQUIRED_DIRS:

            if not (app / folder).exists():

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.CRITICAL,

                        file=str(app / folder),

                        line=None,

                        rule="TZ001",

                        message=f"Pasta '{folder}' inexistente.",

                        recommendation="Criar a pasta.",

                    )

                )