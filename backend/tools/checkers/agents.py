from pathlib import Path

from tools.core.checker import Checker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class AgentsChecker(Checker):

    NAME = "Agents"

    DESCRIPTION = "Agent Validation"

    VERSION = "1.0"

    def run(
        self,
        report: AuditReport,
    ):

        folder = Path("app/agents")

        for file in folder.glob("*.py"):

            if file.name.startswith("__"):
                continue

            text = file.read_text(
                encoding="utf8"
            )

            if "class " not in text:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.WARNING,

                        file=str(file),

                        line=None,

                        rule="TZ009",

                        message="Arquivo sem classe Agent.",

                        recommendation="Padronizar Agent.",

                    )

                )

            if "execute(" not in text:

                report.add(

                    Finding(

                        checker=self.NAME,

                        severity=Severity.ERROR,

                        file=str(file),

                        line=None,

                        rule="TZ010",

                        message="Agent sem método execute().",

                        recommendation="Implementar execute().",

                    )

                )