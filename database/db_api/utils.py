from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Group, Schedule, Studio
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


async def group_not_in_studio(
        session: AsyncSession,
        group_name: str,
        studio_id: int
) -> Group:
    """Group not in studio's group list."""

    studio = await session.get(Studio, studio_id)
    for gr in studio.groups:
        if gr.name == group_name:
            raise EntityAlreadyExists
    return None


async def get_schedule(session: AsyncSession, group: Group) -> Schedule:
    """Get schedule by group."""

    stmt = select(Schedule).where(Schedule.group_id == group.id)
    schedule = await session.execute(stmt)
    schedule = schedule.scalar_one_or_none()
    if not schedule:
        raise DoesNotExist
    return schedule
