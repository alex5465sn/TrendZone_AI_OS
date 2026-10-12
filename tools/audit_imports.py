"""Auditoria de consistencia do TrendZone AI OS.

Verifica:
1. Todo `from app.X.Y import Z` resolve para um arquivo real
2. O simbolo Z esta definido no modulo de destino
3. Todo router importado em main.py e registrado
4. Classes de servico usadas existem nos seus modulos
"""
import ast
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "backend" / "app"

problems = []
checked = 0


def module_to_path(dotted: str) -> Path | None:
    parts = dotted.split(".")
    base = ROOT / "backend"
    candidate = base.joinpath(*parts)
    if candidate.with_suffix(".py").exists():
        return candidate.with_suffix(".py")
    if (candidate / "__init__.py").exists():
        return candidate / "__init__.py"
    return None


def iter_py_files():
    for dirpath, dirnames, filenames in os.walk(APP):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            if fn.endswith(".py"):
                yield Path(dirpath) / fn


def defined_names(tree) -> set:
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                names.add(node.target.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                names.add(a.asname or a.name.split(".")[0])
    return names


for py in iter_py_files():
    try:
        tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
    except SyntaxError as e:
        problems.append(f"[SINTAXE] {py}: {e}")
        continue

    checked += 1
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module is None or not node.module.startswith("app."):
            continue

        target = module_to_path(node.module)
        if target is None:
            problems.append(
                f"[MODULO AUSENTE] {py.relative_to(ROOT)}: "
                f"from {node.module} import ... -> arquivo nao existe"
            )
            continue

        # __init__.py pode re-exportar; nao aprofundar aqui
        if target.name == "__init__.py":
            continue

        try:
            target_tree = ast.parse(target.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        available = defined_names(target_tree)
        for alias in node.names:
            name = alias.name
            if name == "*":
                continue
            if name not in available:
                problems.append(
                    f"[SIMBOLO AUSENTE] {py.relative_to(ROOT)}: "
                    f"from {node.module} import {name} — '{name}' nao esta definido em {target.relative_to(ROOT)}"
                )

# main.py: routers importados vs registrados
main_py = APP / "main.py"
main_tree = ast.parse(main_py.read_text(encoding="utf-8"))
imported_routers = {}
for node in ast.walk(main_tree):
    if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("app."):
        for a in node.names:
            if a.name.startswith("router"):
                imported_routers[a.asname or a.name] = node.module

include_calls = [
    n.func.attr if isinstance(n.func, ast.Attribute) else ""
    for n in ast.walk(main_tree)
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "include_router"
]
registered = set()
for n in ast.walk(main_tree):
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "include_router":
        for arg in n.args:
            if isinstance(arg, ast.Name):
                registered.add(arg.id)

for local_name, module in imported_routers.items():
    if local_name not in registered:
        problems.append(f"[ROUTER NAO REGISTRADO] main.py: '{local_name}' (de {module}) importado mas nunca incluido via include_router")

print(f"Arquivos analisados: {checked}")
print(f"Routers importados no main.py: {len(imported_routers)} | registrados: {len(registered)}")
print(f"Problemas encontrados: {len(problems)}")
for p in problems:
    print("  " + p)
sys.exit(1 if problems else 0)
