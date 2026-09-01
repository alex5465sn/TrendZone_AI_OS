"""
TrendZone AI OS
================================

Checker Loader

Responsável por registrar
automaticamente todos os
Checkers disponíveis.
"""

from tools.architecture import ArchitectureChecker
from tools.dependency import DependencyChecker
from tools.imports import ImportsChecker
from tools.models import ModelsChecker


class CheckerLoader:

    @staticmethod
    def load():

        return [

            ArchitectureChecker,

            ImportsChecker,

            DependencyChecker,

            ModelsChecker,

        ]