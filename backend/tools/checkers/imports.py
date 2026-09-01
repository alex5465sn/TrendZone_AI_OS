from pathlib import Path

from tools.core.checker import Checker
from tools.core.report import AuditReport
from tools.core.finding import Finding
from tools.core.severity import Severity


class ImportsChecker(Checker):

    NAME = "Imports"

    DESCRIPTION = "Importações"

    VERSION = "1.0"

    def run(
        self,
        report: AuditReport,
    ):

        for file in Path("app").rglob("*.py"):

            text = file.read_text(
                encoding="utf8"
            )

            if "import *" in text:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.WARNING,

                        file=str(file),

                        line=None,

                        rule="TZ002",

                        message="Wildcard import encontrado.",

                        recommendation="Usar import explícito.",

                    )

                )