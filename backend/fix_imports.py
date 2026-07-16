from pathlib import Path

ROOT = Path(__file__).parent / "app"

print("=" * 60)
print("TrendZone AI OS - Import Fixer")
print("=" * 60)

updated = 0

for file in ROOT.rglob("*.py"):

    text = file.read_text(encoding="utf-8")

    new_text = (
        text
        .replace("from backend.app.", "from app.")
        .replace("import backend.app.", "import app.")
    )

    if text != new_text:

        file.write_text(
            new_text,
            encoding="utf-8"
        )

        print(f"✓ {file.relative_to(ROOT.parent)}")

        updated += 1

print()

print("=" * 60)
print(f"Arquivos atualizados: {updated}")
print("=" * 60)