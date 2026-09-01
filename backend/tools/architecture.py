"""
TrendZone AI OS
================================

Architecture Checker

Valida a arquitetura geral do
projeto TrendZone AI OS.

Verifica:

- Estrutura de diretórios
- Camadas obrigatórias
- Organização Enterprise
"""

from pathlib import Path


class ArchitectureChecker:

    NAME = "Architecture"

    REQUIRED_DIRS = [

        "app/core",

        "app/database",

        "app/security",

        "app/models",

        "app/schemas",

        "app/repositories",

        "app/services",

        "app/agents",

        "app/tasks",

        "app/api",

        "app/integrations",

    ]

    @classmethod
    def run(cls, report):

        warnings = []

        success = True

        for directory in cls.REQUIRED_DIRS:

            if not Path(directory).exists():

                success = False

                warnings.append(

                    f"Diretório ausente: {directory}"

                )

        report.add(

            module=cls.NAME,

            success=success,

            message="Arquitetura validada.",

            warnings=warnings,

        )