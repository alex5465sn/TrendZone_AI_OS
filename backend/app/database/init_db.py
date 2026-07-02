from backend.app.database.base import Base
from backend.app.database.session import engine

# Importa os modelos para que o SQLAlchemy conheça todas as tabelas
from backend.app.models.system_info import SystemInfo


def init_database():
    Base.metadata.create_all(bind=engine)