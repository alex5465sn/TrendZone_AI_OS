from pathlib import Path

from tools.core.checker import Checker
from tools.core.finding import Finding
from tools.core.report import AuditReport
from tools.core.severity import Severity


class DependencyChecker(Checker):

    NAME = "Dependency"

    DESCRIPTION = "Dependency Validation"

    VERSION = "1.0"

    FORBIDDEN = {

        "app.api": [
            "app.database",
        ],

        "app.models": [
            "app.api",
            "app.services",
        ],

        "app.repositories": [
            "app.api",
        ],
    }

    def run(
        self,
        report: AuditReport,
    ):

        for file in Path("app").rglob("*.py"):

            text = file.read_text(
                encoding="utf8"
            )

            module = str(file).replace("\\", ".")

            for source, forbidden in self.FORBIDDEN.items():

                if source not in module:
                    continue

                for target in forbidden:

                    if target in text:

                        report.add(

                            Finding(

                                checker=self.NAME,

                                severity=Severity.ERROR,

                                file=str(file),

                                line=None,

                                rule="TZ003",

                                message=f"Dependência proibida: {target}",

                                recommendation="Remover acoplamento.",

                            )

                        )