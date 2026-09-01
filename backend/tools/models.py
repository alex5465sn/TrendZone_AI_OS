"""
TrendZone AI OS
================================

Models Checker

Valida os Models oficiais.
"""

from pathlib import Path


class ModelsChecker:

    NAME = "Models"

    REQUIRED = [

        "__tablename__",

        "class",

    ]

    @classmethod
    def run(cls, report):

        success = True

        warnings = []

        models = Path("app/models")

        if not models.exists():

            report.add(

                cls.NAME,

                False,

                "Pasta models inexistente.",

            )

            return

        for file in models.glob("*.py"):

            if file.name == "__init__.py":
                continue

            text = file.read_text(
                encoding="utf-8"
            )

            for item in cls.REQUIRED:

                if item not in text:

                    success = False

                    warnings.append(

                        f"{file.name}: ausência de {item}"

                    )

        report.add(

            module=cls.NAME,

            success=success,

            message="Models verificados.",

            warnings=warnings,

        )