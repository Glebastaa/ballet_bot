from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Подключение к базе.
engine = create_async_engine(
    url=settings.DATABASE_url_asyncpg,
    echo=settings.DEBUG
)
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False
)

naming_convention = {
      "ix": "ix_%(column_0_label)s",
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s",
    }


# Базовый класс для моделей и миграций.
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)
