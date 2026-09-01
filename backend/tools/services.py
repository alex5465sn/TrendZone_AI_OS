"""
TrendZone AI OS
================================

Services Checker

Valida regras de negócio.
"""

from pathlib import Path

from tools.base_checker import BaseChecker


class ServicesChecker(BaseChecker):

    NAME = "Services"

    DESCRIPTION = "Valida os Services."

    @classmethod
    def run(cls, report):

        success = True

        warnings = []

        path = Path("app/services")

        for file in path.glob("*.py"):

            text = file.read_text(
                encoding="utf-8"
            )

            if "Repository" not in text:

                warnings.append(

                    f"{file.name}: não utiliza Repository."

                )

            if "raise ValueError" not in text:

                warnings.append(

                    f"{file.name}: não possui validações."

                )

        report.add(

            module=cls.NAME,

            success=success,

            message="Services auditados.",

            warnings=warnings,

        )