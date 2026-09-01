from pathlib import Path

from tools.core.checker import Checker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class TasksChecker(Checker):

    NAME = "Tasks"

    DESCRIPTION = "Task Validation"

    VERSION = "1.0"

    def run(
        self,
        report: AuditReport,
    ):

        folder = Path("app/tasks")

        for file in folder.glob("*.py"):

            if file.name.startswith("__"):
                continue

            text = file.read_text(
                encoding="utf8"
            )

            if "__main__" not in text:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.INFO,

                        file=str(file),

                        line=None,

                        rule="TZ011",

                        message="Task sem execução direta.",

                        recommendation="Adicionar bloco __main__.",

                    )

                )

            if "logging" not in text:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.WARNING,

                        file=str(file),

                        line=None,

                        rule="TZ012",

                        message="Task sem logging.",

                        recommendation="Utilizar logger central.",

                    )

                )