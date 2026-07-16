"""
TrendZone AI OS
===============================

Schemas Oficiais da Aplicação.

Este módulo centraliza todos os Schemas
utilizados pelo FastAPI.

Sempre importe através deste package.

Exemplo:

from app.schemas import ProductCreate
from app.schemas import UserResponse
"""

from app.schemas.auth import *
from app.schemas.pipeline import *
from app.schemas.product import *
from app.schemas.system_info import *
from app.schemas.user import *