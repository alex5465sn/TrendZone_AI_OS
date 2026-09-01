"""
TrendZone AI OS
================================

Dependency Checker

Valida dependências entre
as camadas do sistema.

Arquitetura oficial:

API
↓

Services
↓

Repositories
↓

Models
"""

from pathlib import Path


class DependencyChecker:

    NAME = "Dependencies"

    RULES = {

        "app/api": [
            "app.services",
            "app.schemas",
            "app.security",
            "app.database",
            "app.api",
        ],

        "app/services": [
            "app.repositories",
            "app.models",
            "app.schemas",
            "app.services",
        ],

        "app/repositories": [
            "app.models",
            "app.database",
            "sqlalchemy",
        ],

        "app/models": [
            "sqlalchemy",
            "datetime",
            "uuid",
            "typing",
        ],
    }

    @classmethod
    def run(cls, report):

        warnings = []

        success = True

        for directory, allowed in cls.RULES.items():

            path = Path(directory)

            if not path.exists():
                continue

            for file in path.glob("*.py"):

                lines = file.read_text(
                    encoding="utf-8"
                ).splitlines()

                for number, line in enumerate(lines, start=1):

                    line = line.strip()

                    if not (
                        line.startswith("import")
                        or line.startswith("from")
                    ):
                        continue

                    valid = False

                    for package in allowed:

                        if package in line:
                            valid = True
                            break

                    if "from app." not in line:
                        valid = True

                    if not valid:

                        success = False

                        warnings.append(

                            f"{file}:{number} -> {line}"

                        )

        report.add(

            module=cls.NAME,

            success=success,

            message="Dependências verificadas.",

            warnings=warnings,

        )