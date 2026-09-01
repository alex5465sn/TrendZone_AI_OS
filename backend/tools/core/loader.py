"""
TrendZone AI OS

Automatic Checker Loader
"""

from pathlib import Path
import importlib
import inspect

from tools.core.checker import Checker
from tools.core.registry import CheckerRegistry


class CheckerLoader:

    @staticmethod
    def build() -> CheckerRegistry:

        registry = CheckerRegistry()

        checkers_path = Path(__file__).parent.parent / "checkers"

        for file in checkers_path.glob("*.py"):

            if file.stem.startswith("_"):
                continue

            module = importlib.import_module(
                f"tools.checkers.{file.stem}"
            )

            for _, obj in inspect.getmembers(
                module,
                inspect.isclass,
            ):

                if (
                    issubclass(obj, Checker)
                    and obj is not Checker
                ):

                    registry.register(obj())

        return registry