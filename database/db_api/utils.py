from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Group, Schedule, Studio
from exceptions import DoesNotExist


async def get_by_name(
        entety_cls: Any,
        name: str,
        session: AsyncSession
) -> Any | None:
    """Get instance by name."""

    stmt = select(entety_cls).where(entety_cls.name.ilike(name))
    instance = await session.execute(stmt)
    return instance.scalar_one_or_none()


async def get_group_by_name_and_studio(
        session: AsyncSession,
        group_name: str,
        studio_name: str
) -> Group:
    """Get specific group."""

    studio = await get_by_name(Studio, studio_name, session)
    group = None
    for gr in studio.groups:
        if gr.name == group_name:
            group = gr
    if not group:
        raise DoesNotExist
    return group


async def get_schedule(session: AsyncSession, group: Group) -> Schedule:
    """Get schedule by group."""

    stmt = select(Schedule).where(Schedule.group_id == group.id)
    schedule = await session.execute(stmt)
    schedule = schedule.scalar_one_or_none()
    if not schedule:
        raise DoesNotExist
    return schedule