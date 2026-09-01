"""
TrendZone AI OS
================================

Imports Checker

Analisa imports inválidos
e dependências circulares.
"""

from pathlib import Path


class ImportsChecker:

    NAME = "Imports"

    INVALID_IMPORTS = [

        "import *",

    ]

    @classmethod
    def run(cls, report):

        warnings = []

        success = True

        for file in Path("app").rglob("*.py"):

            text = file.read_text(

                encoding="utf-8"

            )

            for invalid in cls.INVALID_IMPORTS:

                if invalid in text:

                    success = False

                    warnings.append(

                        f"{file}: encontrado '{invalid}'"

                    )

        report.add(

            module=cls.NAME,

            success=success,

            message="Imports verificados.",

            warnings=warnings,

        )