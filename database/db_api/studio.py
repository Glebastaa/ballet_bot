from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.db_api.utils import get_by_name

from database.models import Studio
from exceptions import DoesNotExist, EntityAlreadyExists


async def add_studio(session: AsyncSession, studio_name: str) -> Studio:
    """Create a new studio."""

    if await get_by_name(Studio, studio_name, session):
        raise EntityAlreadyExists
    studio = Studio(name=studio_name)
    result = session.add(studio)
    await session.commit()
    return result


async def get_studios(session: AsyncSession) -> list[Studio]:
    """Get studios."""

    stmt = select(Studio).order_by(Studio.id)
    studios = await session.execute(stmt)
    return studios.scalars().all()


async def edit_studio(
        session: AsyncSession,
        studio_id: int,
        new_studio_name: str
) -> Studio:
    """Change studio's name."""

    studio = await session.get(Studio, studio_id)
    if not studio:
        raise DoesNotExist
    studio.name = new_studio_name
    await session.commit()
    return studio


async def delete_studio(session: AsyncSession, studio_id: int) -> str:
    "Delete the studio."

    studio = await session.get(Studio, studio_id)
    await session.delete(studio)
    await session.commit()
    return studio.name