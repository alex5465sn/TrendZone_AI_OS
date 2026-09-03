"""
TrendZone AI OS
================================

Migrações leves e idempotentes para o SQLite.

Objetivo: tornar o schema multi-marketplace com segurança,
sem perder dados e sem exigir instalação de alembic.

1. products  -> coluna marketplace + UNIQUE(marketplace, item_id)
2. sales     -> coluna marketplace + UNIQUE(marketplace, conversion_id)
3. campaigns / prospects / schedules -> coluna marketplace

Tabelas com restrição UNIQUE global precisam ser reconstruídas
(rename -> create -> copy -> drop), preservando os ids originais
(e portanto as FKs de outras tabelas).

Importante: os models precisam estar carregados para o
Base.metadata.create_all criar as tabelas — por isso este
módulo importa app.models explicitamente.
"""

import logging

from sqlalchemy import Engine, inspect, text

# Garante que todos os models estejam registrados no metadata
import app.models  # noqa: F401
from app.database.base import Base

logger = logging.getLogger("trendzone.migrations")

UNIQUE_REBUILD = {
    "products": {
        "legacy": "products_legacy",
        "check_col": "marketplace",
    },
    "sales": {
        "legacy": "sales_legacy",
        "check_col": "marketplace",
    },
}

ADD_COLUMN_TABLES = [
    "campaigns",
    "prospects",
    "schedules",
]

EXTRA_COLUMNS = {
    "sales": [
        ("user_id", "INTEGER NULL"),
    ],
}


def _table_exists(conn, name: str) -> bool:
    return inspect(conn).has_table(name)


def _columns(conn, table: str) -> list[str]:
    insp = inspect(conn)
    return [c["name"] for c in insp.get_columns(table)]


def _rebuild(engine: Engine, table: str, legacy: str) -> None:
    """Reconstrói a tabela a partir do model atual, copiando os dados.

    Executa cada fase em uma conexão própria (com commit entre fases)
    para evitar caches de reflection e limitações de DDL do SQLite.
    """
    # ---------------- Fase 1: estado atual ----------------
    with engine.begin() as conn:
        conn.exec_driver_sql("PRAGMA legacy_alter_table=ON")
        has_table = _table_exists(conn, table)
        has_legacy = _table_exists(conn, legacy)
        marketplace_ok = has_table and "marketplace" in _columns(conn, table)

    # Banco novo (nenhuma tabela ainda): create_all em main.py cria tudo.
    if not has_table and not has_legacy:
        logger.info("Migração %s: banco novo, nada a reconstruir.", table)
        return

    # Migração já concluída em execução anterior: descarta a tabela legada.
    if has_table and has_legacy and marketplace_ok:
        with engine.begin() as conn:
            conn.exec_driver_sql(f'DROP TABLE IF EXISTS "{legacy}"')
        logger.info(
            "Migração %s: conclusão de execução anterior (legacy descartada).",
            table,
        )
        return

    # Já migrada e sem legacy.
    if has_table and not has_legacy and marketplace_ok:
        logger.info("Migração %s: schema já multi-marketplace.", table)
        return

    # Tabela antiga existe (sem marketplace): renomeia para legacy.
    if has_table and not has_legacy:
        with engine.begin() as conn:
            conn.exec_driver_sql("PRAGMA legacy_alter_table=ON")
            conn.exec_driver_sql(f"ALTER TABLE {table} RENAME TO {legacy}")
        logger.info("Migração %s: tabela antiga renomeada para %s", table, legacy)
        has_legacy = True

    if not has_legacy:
        raise RuntimeError(
            f"Migração {table}: estado inesperado (sem tabela origem)."
        )

    # ---------------- Fase 2: remove índices nomeados da legada ----------------
    with engine.begin() as conn:
        idx_rows = conn.execute(
            text(
                "SELECT name FROM sqlite_master "
                "WHERE type='index' AND tbl_name=:t AND sql IS NOT NULL"
            ),
            {"t": legacy},
        ).fetchall()
        for (idx_name,) in idx_rows:
            conn.exec_driver_sql(f'DROP INDEX IF EXISTS "{idx_name}"')
        logger.info(
            "Migração %s: índices da tabela legada removidos (%d)",
            table,
            len(idx_rows),
        )

    # ---------------- Fase 3: cria a tabela nova (schema do model) ----------------
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)

    # ---------------- Fase 4: copia dados e remove legada ----------------
    with engine.begin() as conn:
        shared = [
            c for c in _columns(conn, legacy) if c in _columns(conn, table)
        ]
        shared_sql = ", ".join(f'"{c}"' for c in shared)
        total = conn.execute(
            text(f'SELECT COUNT(*) FROM "{legacy}"')
        ).scalar()
        conn.exec_driver_sql(
            f'INSERT INTO "{table}" ({shared_sql}, "marketplace") '
            f'SELECT {shared_sql}, \'shopee\' FROM "{legacy}"'
        )
        conn.exec_driver_sql(f'DROP TABLE "{legacy}"')
        logger.info(
            "Migração %s: %s registros copiados e tabela legada removida.",
            table,
            total,
        )


def _add_marketplace_column(engine: Engine, table: str) -> None:
    with engine.begin() as conn:
        if not _table_exists(conn, table):
            return
        if "marketplace" in _columns(conn, table):
            return
        conn.exec_driver_sql(
            f'ALTER TABLE "{table}" '
            "ADD COLUMN marketplace VARCHAR(30) NOT NULL DEFAULT 'shopee'"
        )
        logger.info("Migração: coluna marketplace adicionada em %s", table)


def _add_columns(engine: Engine, table: str, columns: list[tuple[str, str]]) -> None:
    with engine.begin() as conn:
        if not _table_exists(conn, table):
            return
        existing = _columns(conn, table)
        for name, ddl in columns:
            if name in existing:
                continue
            conn.exec_driver_sql(
                f'ALTER TABLE "{table}" ADD COLUMN "{name}" {ddl}'
            )
            logger.info("Migração: coluna %s adicionada em %s", name, table)


def run(engine: Engine) -> None:
    for table, cfg in UNIQUE_REBUILD.items():
        try:
            _rebuild(engine, table, cfg["legacy"])
        except Exception:
            logger.exception("Falha na migração da tabela %s", table)
            raise

    for table in ADD_COLUMN_TABLES:
        try:
            _add_marketplace_column(engine, table)
        except Exception:
            logger.exception("Falha ao adicionar marketplace em %s", table)
            raise

    for table, columns in EXTRA_COLUMNS.items():
        try:
            _add_columns(engine, table, columns)
        except Exception:
            logger.exception("Falha ao adicionar colunas extras em %s", table)
            raise

    logger.info("Migrações multi-marketplace concluídas.")
