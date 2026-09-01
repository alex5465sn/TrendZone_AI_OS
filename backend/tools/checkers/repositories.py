from pathlib import Path

from tools.core.checker import Checker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class RepositoriesChecker(Checker):

    NAME = "Repositories"

    DESCRIPTION = "Repository Validation"

    VERSION = "1.0"

    REQUIRED_METHODS = [

        "create",

        "get_by_id",

        "get_all",

    ]

    def run(
        self,
        report: AuditReport,
    ):

        folder = Path("app/repositories")

        for file in folder.glob("*.py"):

            if file.name == "__init__.py":
                continue

            text = file.read_text(
                encoding="utf8"
            )

            for method in self.REQUIRED_METHODS:

                if f"def {method}" not in text:

                    report.add(

                        Finding(

                            checker=self.NAME,

                            severity=Severity.WARNING,

                            file=str(file),

                            line=None,

                            rule="TZ006",

                            message=f"Método obrigatório '{method}' ausente.",

                            recommendation="Padronizar Repository.",

                        )

                    )