from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Подключение к базе.
engine = create_async_engine(
    url=settings.DATABASE_url_asyncpg,
    echo=False
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Выдача сессий. Не работает, как задумывалось.
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#    async with async_session_maker() as session:
#        yield session


# Базовый класс для моделей и миграций.
class Base(DeclarativeBase):
    pass
