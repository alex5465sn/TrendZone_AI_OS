"""Auditoria de contrato API: frontend vs backend.

Extrai:
- Backend: prefix de cada APIRouter + caminhos dos decorators (@router.get/post/put/delete/patch)
- Frontend: primeiro argumento de getData/postData/putData/deleteData e api.get/post/put/delete/patch

Normaliza parametros ({x}, :x, ${x}) e cruza os conjuntos.
"""
import ast
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend" / "app"
FRONTEND = ROOT / "frontend" / "src"

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "head", "options"}


def norm(path: str) -> str:
    path = re.sub(r"\$\{[^}]+\}", "*", path)
    path = re.sub(r"\{[^}]+\}", "*", path)
    path = re.sub(r":([a-zA-Z_][a-zA-Z0-9_]*)", "*", path)
    return "/" + path.strip("/")


# ---------- BACKEND ----------
backend_routes = set()

for dirpath, dirnames, filenames in os.walk(BACKEND):
    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
    for fn in filenames:
        if not fn.endswith(".py"):
            continue
        p = Path(dirpath) / fn
        src = p.read_text(encoding="utf-8")
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue

        router_prefixes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(call.func, ast.Name) and call.func.id == "APIRouter":
                    for tgt in node.targets:
                        if isinstance(tgt, ast.Name):
                            prefix = ""
                            for kw in call.keywords:
                                if kw.arg == "prefix" and isinstance(kw.value, ast.Constant):
                                    prefix = kw.value.value
                            router_prefixes[tgt.id] = prefix

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for dec in node.decorator_list:
                    if (
                        isinstance(dec, ast.Call)
                        and isinstance(dec.func, ast.Attribute)
                        and dec.func.attr in HTTP_METHODS
                        and isinstance(dec.func.value, ast.Name)
                        and dec.func.value.id in router_prefixes
                    ):
                        path = ""
                        if dec.args and isinstance(dec.args[0], ast.Constant):
                            path = dec.args[0].value
                        full = router_prefixes[dec.func.value.id] + path
                        backend_routes.add(norm(full))
                    elif (
                        isinstance(dec, ast.Call)
                        and isinstance(dec.func, ast.Attribute)
                        and dec.func.attr == "api_route"
                        and isinstance(dec.func.value, ast.Name)
                        and dec.func.value.id in router_prefixes
                    ):
                        path = dec.args[0].value if dec.args and isinstance(dec.args[0], ast.Constant) else ""
                        backend_routes.add(norm(router_prefixes[dec.func.value.id] + path))

# StaticFiles /media
if "media" in (BACKEND / "main.py").read_text(encoding="utf-8"):
    backend_routes.add("/media/*")

# ---------- FRONTEND (regex sobre TypeScript) ----------
frontend_urls = {}

URL_RE = re.compile(
    r"\b(?:getData|postData|putData|deleteData|api\.(?:get|post|put|delete|patch))"
    r"(?:<[^>()]*>)?\(\s*([`\"'])(/[^`\"']*)\1",
    re.DOTALL,
)

for dirpath, dirnames, filenames in os.walk(FRONTEND):
    dirnames[:] = [d for d in dirnames if d not in ("node_modules", "__pycache__")]
    for fn in filenames:
        if not fn.endswith((".ts", ".tsx")):
            continue
        p = Path(dirpath) / fn
        src = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)
        for i, line in enumerate(src.splitlines(), 1):
            for m in URL_RE.finditer(line):
                u = m.group(2).split("?")[0]
                frontend_urls.setdefault(norm(u), set()).add(f"{rel}:{i}")

# ---------- CRUZAMENTO ----------
def url_matches(url: str, route: str) -> bool:
    parts = url.strip("/").split("/")
    rparts = route.strip("/").split("/")
    if len(rparts) != len(parts):
        return False
    return all(rp == "*" or pp == "*" or rp == pp for rp, pp in zip(rparts, parts))


missing = []
for raw_url in sorted(frontend_urls):
    # candidatos: versao com ${...} como wildcard e versao removida (era querystring)
    candidates = {raw_url}
    stripped = re.sub(r"\$\{[^}]*\}\*?$", "", raw_url).rstrip("*")
    if stripped:
        candidates.add(norm(stripped))
    if any(any(url_matches(c, route) for route in backend_routes) for c in candidates):
        continue
    missing.append((raw_url, sorted(frontend_urls[raw_url])))

print(f"Rotas backend: {len(backend_routes)}")
print(f"URLs frontend unicas: {len(frontend_urls)}")
print(f"URLs frontend SEM rota correspondente no backend: {len(missing)}")
for url, locs in missing:
    print(f"  [SEM ROTA] {url}")
    for l in locs[:3]:
        print(f"      -> {l}")
sys.exit(1 if missing else 0)
