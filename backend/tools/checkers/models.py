from pathlib import Path

from tools.core.checker import Checker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class ModelsChecker(Checker):

    NAME = "Models"

    DESCRIPTION = "Model Validation"

    VERSION = "1.0"

    def run(
        self,
        report: AuditReport,
    ):

        folder = Path("app/models")

        for file in folder.glob("*.py"):

            if file.name == "__init__.py":
                continue

            text = file.read_text(
                encoding="utf8"
            )

            if "__tablename__" not in text:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.WARNING,

                        file=str(file),

                        line=None,

                        rule="TZ004",

                        message="Model sem __tablename__.",

                        recommendation="Definir __tablename__.",

                    )

                )

            if "uuid" not in text.lower():

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.INFO,

                        file=str(file),

                        line=None,

                        rule="TZ005",

                        message="Model sem UUID.",

                        recommendation="Adicionar UUID como identificador público.",

                    )

                )