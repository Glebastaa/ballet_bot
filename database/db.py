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


# Базовый класс для моделей и миграций.
class Base(DeclarativeBase):
    pass
