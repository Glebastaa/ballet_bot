import asyncio
from typing import Generator
import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from database.db import Base
from database.models import Student # noqa: for alembic


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    """
    Creates an instance of the default event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def create_db():
    engine = create_async_engine(settings.DATABASE_url_asyncpg)
    print(f"{settings.DATABASE_url_asyncpg}")
    assert settings.MODE == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return engine


@pytest.fixture
async def session(create_db):
    sessionmaker = async_sessionmaker(
        create_db,
        expire_on_commit=False,
        autoflush=False
    )
    async with sessionmaker() as session:
        yield session
