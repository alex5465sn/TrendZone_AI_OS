"""
TrendZone AI OS

AST Utilities
"""

from pathlib import Path
import ast


class ASTUtils:

    @staticmethod
    def parse(file: Path):

        return ast.parse(

            file.read_text(

                encoding="utf8"

            )

        )

    @staticmethod
    def classes(tree):

        return [

            node

            for node in ast.walk(tree)

            if isinstance(node, ast.ClassDef)

        ]

    @staticmethod
    def functions(tree):

        return [

            node

            for node in ast.walk(tree)

            if isinstance(node, ast.FunctionDef)

        ]

    @staticmethod
    def imports(tree):

        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                imports.extend(

                    alias.name

                    for alias in node.names

                )

            elif isinstance(node, ast.ImportFrom):

                imports.append(

                    node.module

                )

        return imports

    @staticmethod
    def calls(tree):

        calls = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    calls.append(

                        node.func.id

                    )

        return calls