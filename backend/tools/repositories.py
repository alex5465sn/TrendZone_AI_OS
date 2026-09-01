"""
TrendZone AI OS
================================

Repositories Checker

Valida os repositórios oficiais.
"""

from pathlib import Path

from tools.base_checker import BaseChecker


class RepositoriesChecker(BaseChecker):

    NAME = "Repositories"

    DESCRIPTION = "Valida os Repositories."

    REQUIRED = [

        "create",

        "update",

        "get",

        "delete",

    ]

    @classmethod
    def run(cls, report):

        success = True

        warnings = []

        path = Path("app/repositories")

        for file in path.glob("*.py"):

            if file.name == "__init__.py":
                continue

            text = file.read_text(
                encoding="utf-8"
            )

            for method in cls.REQUIRED:

                if method not in text:

                    success = False

                    warnings.append(

                        f"{file.name}: método '{method}' ausente."

                    )

        report.add(

            module=cls.NAME,

            success=success,

            message="Repositories auditados.",

            warnings=warnings,

        )