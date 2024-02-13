from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import async_session_maker
from database.models import Studio
from exceptions import DoesNotExist, EntityAlreadyExists


async def get_by_name(
        entety_cls: Any,
        name: str,
        session: AsyncSession
) -> Any | None:
    """Get instance by name."""

    stmt = select(entety_cls).where(entety_cls.name.ilike(name))
    instance = await session.execute(stmt)
    return instance.scalar_one_or_none()


async def add_studio(studio_name: str) -> Studio:
    """Create a new studio."""

    async with async_session_maker() as session:
        if await get_by_name(Studio, studio_name, session):
            raise EntityAlreadyExists
        studio = Studio(name=studio_name)
        result = session.add(studio)
        await session.commit()
        return result


async def get_studios() -> list[Studio]:
    """Get studios."""

    stmt = select(Studio).order_by(Studio.id)
    async with async_session_maker() as session:
        studios = await session.execute(stmt)
        return studios.scalars().all()


async def edit_studio(studio_name: str, new_studio_name: str) -> Studio:
    """Change studio's name."""

    async with async_session_maker() as session:
        studio = await get_by_name(Studio, studio_name, session)
        if not studio:
            raise DoesNotExist
        studio.name = new_studio_name
        await session.commit()
        return studio


async def delete_studio(studio_name: str) -> str:
    "Delete the studio."

    async with async_session_maker() as session:
        studio = await get_by_name(Studio, studio_name, session)
        await session.delete(studio)
        await session.commit()
        return studio_name
