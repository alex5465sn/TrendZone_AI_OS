from pathlib import Path

from tools.core.checker import Checker
from tools.core.ast_utils import ASTUtils


class PythonProjectChecker(Checker):

    ROOT = Path("app")

    def python_files(self):

        return self.ROOT.rglob("*.py")

    def parse(self, file):

        return ASTUtils.parse(file)

    def classes(self, tree):

        return ASTUtils.classes(tree)

    def functions(self, tree):

        return ASTUtils.functions(tree)

    def imports(self, tree):

        return ASTUtils.imports(tree)

    def calls(self, tree):

        return ASTUtils.calls(tree)