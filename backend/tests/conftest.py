"""
Configuracao compartilhada dos testes automatizados.

Usa um banco SQLite em memoria, isolado do banco de dados real
(trendzone.db), para nao afetar dados de producao/dev durante os
testes.
"""

import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database.base import Base  # noqa: E402

import app.models  # noqa: E402,F401


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
    )

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()
