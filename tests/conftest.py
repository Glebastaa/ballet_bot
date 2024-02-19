import asyncio
from typing import Generator
import pytest

from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from database.db import Base, engine, async_session_maker
from database.models import Student # noqa


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    """
    Creates an instance of the default event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def create_db():
    engine = create_async_engine(settings.DATABASE_url_asyncpg)
    print(f"{settings.DATABASE_url_asyncpg}")
    assert settings.MODE == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print('end!!!!!!!!')


@pytest.fixture
async def session():
    async with async_session_maker() as session:
        yield session
