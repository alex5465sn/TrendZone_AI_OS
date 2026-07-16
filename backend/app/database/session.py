from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings


DATABASE_URL = settings.DATABASE_URL


engine = create_engine(

    DATABASE_URL,

    echo=False,

    future=True,

    pool_pre_ping=True,

)


SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine,

    expire_on_commit=False,

)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()