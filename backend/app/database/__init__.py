"""
TrendZone AI OS
================================

Database Package

Centraliza a exportação dos componentes
da camada de banco de dados.

Sempre importe através deste módulo.

Exemplo:

from app.database import get_db
from app.database import SessionLocal
from app.database import engine
"""

from app.database.session import (
    SessionLocal,
    engine,
    get_db,
)

from app.database.base import Base

__all__ = (

    "Base",

    "SessionLocal",

    "engine",

    "get_db",

)