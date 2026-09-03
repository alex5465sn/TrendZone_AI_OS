"""
TrendZone AI OS — Inspector Service

Agente inspetor que varre o proprio codigo
e logs da plataforma, detecta problemas e
tenta corrigir automaticamente quando possivel.

Cada verificacao retorna um dict com:
  - file: caminho do arquivo
  - line: numero da linha (quando aplicavel)
  - severity: "error" | "warning" | "info"
  - message: descricao do problema
  - fixed: bool — se foi auto-corrigido
  - fix_detail: o que foi feito (quando fixed=True)
"""

import ast
import os
import re
import importlib
import traceback
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("trendzone")

BACKEND_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = BACKEND_ROOT / "app"


class InspectorService:

    @classmethod
    def full_inspection(cls) -> list[dict[str, Any]]:
        results: list[dict] = []
        results.extend(cls.check_python_syntax())
        results.extend(cls.check_imports())
        results.extend(cls.check_models_registered())
        results.extend(cls.check_routes_registered())
        results.extend(cls.check_env_vars())
        results.extend(cls.check_database())
        results.extend(cls.check_logs())
        return results

    @classmethod
    def check_python_syntax(cls) -> list[dict]:
        results = []
        for py_file in APP_ROOT.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            rel = py_file.relative_to(BACKEND_ROOT)
            try:
                source = py_file.read_text(encoding="utf-8")
                ast.parse(source, filename=str(rel))
            except SyntaxError as e:
                results.append({
                    "file": str(rel),
                    "line": e.lineno or 0,
                    "severity": "error",
                    "message": f"Erro de sintaxe: {e.msg}",
                    "fixed": False,
                    "fix_detail": "",
                })
            except Exception as e:
                results.append({
                    "file": str(rel),
                    "line": 0,
                    "severity": "error",
                    "message": f"Erro ao ler arquivo: {e}",
                    "fixed": False,
                    "fix_detail": "",
                })
        if not results:
            results.append({
                "file": "app/",
                "line": 0,
                "severity": "info",
                "message": "Todos os arquivos Python tem sintaxe valida.",
                "fixed": False,
                "fix_detail": "",
            })
        return results

    @classmethod
    def check_imports(cls) -> list[dict]:
        results = []
        for py_file in APP_ROOT.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            rel = py_file.relative_to(BACKEND_ROOT)
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source)
            except Exception:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        cls._check_module(alias.name, str(rel), node.lineno, results)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        cls._check_module(node.module, str(rel), node.lineno, results)
        if not any(r["severity"] == "error" for r in results):
            results.append({
                "file": "app/",
                "line": 0,
                "severity": "info",
                "message": "Todos os imports resolvem corretamente.",
                "fixed": False,
                "fix_detail": "",
            })
        return results

    @classmethod
    def _check_module(cls, module_name: str, file: str, line: int, results: list):
        top = module_name.split(".")[0]
        if top in ("app",):
            mod_path = APP_ROOT.parent / module_name.replace(".", os.sep)
            if not (mod_path.exists() or mod_path.with_suffix(".py").exists()
                    or (mod_path / "__init__.py").exists()):
                results.append({
                    "file": file,
                    "line": line,
                    "severity": "error",
                    "message": f"Import '{module_name}' nao encontrado no projeto.",
                    "fixed": False,
                    "fix_detail": "",
                })

    @classmethod
    def check_models_registered(cls) -> list[dict]:
        results = []
        init_path = APP_ROOT / "models" / "__init__.py"
        if not init_path.exists():
            results.append({
                "file": "app/models/__init__.py",
                "line": 0,
                "severity": "error",
                "message": "Arquivo __init__.py de models nao encontrado.",
                "fixed": False,
                "fix_detail": "",
            })
            return results

        init_content = init_path.read_text(encoding="utf-8")

        models_dir = APP_ROOT / "models"
        for model_file in models_dir.glob("*.py"):
            if model_file.name.startswith("_"):
                continue
            module_name = model_file.stem
            class_name = module_name.title().replace("_", "")
            if module_name == "system_info":
                class_name = "SystemInfo"

            if f"from app.models.{module_name}" not in init_content:
                results.append({
                    "file": "app/models/__init__.py",
                    "line": 0,
                    "severity": "warning",
                    "message": f"Model '{module_name}.py' existe mas nao esta registrado em __init__.py.",
                    "fixed": False,
                    "fix_detail": "",
                })

        if not any(r["severity"] in ("error", "warning") for r in results):
            results.append({
                "file": "app/models/__init__.py",
                "line": 0,
                "severity": "info",
                "message": "Todos os models estao registrados corretamente.",
                "fixed": False,
                "fix_detail": "",
            })
        return results

    @classmethod
    def check_routes_registered(cls) -> list[dict]:
        results = []
        main_path = APP_ROOT / "main.py"
        if not main_path.exists():
            return results

        main_content = main_path.read_text(encoding="utf-8")

        api_dir = APP_ROOT / "api"
        skip_files = {
            "response.py", "__init__.py", "exception_handler.py",
            "middleware.py", "router.py", "init.py",
        }
        for api_file in api_dir.glob("*.py"):
            if api_file.name.startswith("_") or api_file.name in skip_files:
                continue
            module_name = api_file.stem
            if f"from app.api.{module_name}" not in main_content:
                results.append({
                    "file": "app/main.py",
                    "line": 0,
                    "severity": "warning",
                    "message": f"Router 'app/api/{module_name}.py' existe mas nao esta incluido em main.py.",
                    "fixed": False,
                    "fix_detail": "",
                })

        if not any(r["severity"] in ("error", "warning") for r in results):
            results.append({
                "file": "app/main.py",
                "line": 0,
                "severity": "info",
                "message": "Todos os routers estao registrados corretamente.",
                "fixed": False,
                "fix_detail": "",
            })
        return results

    @classmethod
    def check_env_vars(cls) -> list[dict]:
        results = []
        env_path = BACKEND_ROOT.parent / ".env"
        if not env_path.exists():
            results.append({
                "file": ".env",
                "line": 0,
                "severity": "error",
                "message": "Arquivo .env nao encontrado na raiz do projeto.",
                "fixed": False,
                "fix_detail": "",
            })
            return results

        content = env_path.read_text(encoding="utf-8")
        required = ["SECRET_KEY", "DATABASE_URL", "SHOPEE_APP_ID", "SHOPEE_SECRET"]
        for var in required:
            pattern = rf"^{var}\s*=\s*\S+"
            if not re.search(pattern, content, re.MULTILINE):
                results.append({
                    "file": ".env",
                    "line": 0,
                    "severity": "warning",
                    "message": f"Variavel de ambiente '{var}' esta vazia ou ausente.",
                    "fixed": False,
                    "fix_detail": "",
                })

        if not any(r["severity"] in ("error", "warning") for r in results):
            results.append({
                "file": ".env",
                "line": 0,
                "severity": "info",
                "message": "Todas as variaveis de ambiente obrigatorias estao configuradas.",
                "fixed": False,
                "fix_detail": "",
            })
        return results

    @classmethod
    def check_database(cls) -> list[dict]:
        results = []
        db_path = BACKEND_ROOT / "trendzone.db"
        if not db_path.exists():
            results.append({
                "file": "trendzone.db",
                "line": 0,
                "severity": "error",
                "message": "Banco de dados SQLite nao encontrado.",
                "fixed": False,
                "fix_detail": "",
            })
            return results

        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            tables = [r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()]
            conn.close()

            expected = ["users", "products", "campaigns", "prospects", "schedules", "sales"]
            for table in expected:
                if table not in tables:
                    results.append({
                        "file": "trendzone.db",
                        "line": 0,
                        "severity": "warning",
                        "message": f"Tabela '{table}' nao encontrada no banco. Sera criada ao reiniciar o backend.",
                        "fixed": False,
                        "fix_detail": "",
                    })

            if not any(r["severity"] in ("error", "warning") for r in results):
                results.append({
                    "file": "trendzone.db",
                    "line": 0,
                    "severity": "info",
                    "message": f"Banco OK — {len(tables)} tabela(s): {', '.join(tables)}.",
                    "fixed": False,
                    "fix_detail": "",
                })
        except Exception as e:
            results.append({
                "file": "trendzone.db",
                "line": 0,
                "severity": "error",
                "message": f"Erro ao acessar banco: {e}",
                "fixed": False,
                "fix_detail": "",
            })
        return results

    @classmethod
    def check_logs(cls) -> list[dict]:
        results = []
        log_path = BACKEND_ROOT / "logs" / "trendzone.log"
        if not log_path.exists():
            results.append({
                "file": "logs/trendzone.log",
                "line": 0,
                "severity": "info",
                "message": "Arquivo de log nao encontrado (normal em primeira execucao).",
                "fixed": False,
                "fix_detail": "",
            })
            return results

        try:
            content = log_path.read_text(encoding="utf-8", errors="replace")
            lines = content.strip().split("\n")
            errors = [
                (i + 1, line) for i, line in enumerate(lines)
                if "ERROR" in line or "CRITICAL" in line or "Traceback" in line
            ]

            if errors:
                last_errors = errors[-5:]
                for line_num, line_text in last_errors:
                    results.append({
                        "file": "logs/trendzone.log",
                        "line": line_num,
                        "severity": "warning",
                        "message": f"Erro no log: {line_text[:200]}",
                        "fixed": False,
                        "fix_detail": "",
                    })
            else:
                results.append({
                    "file": "logs/trendzone.log",
                    "line": 0,
                    "severity": "info",
                    "message": f"Log limpo — {len(lines)} linha(s), sem erros.",
                    "fixed": False,
                    "fix_detail": "",
                })
        except Exception as e:
            results.append({
                "file": "logs/trendzone.log",
                "line": 0,
                "severity": "error",
                "message": f"Erro ao ler log: {e}",
                "fixed": False,
                "fix_detail": "",
            })
        return results
