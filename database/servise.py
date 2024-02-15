from datetime import time
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Group, Schedule, Studio, WeekDays
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


# Studios.
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
        studio_name: str,
        new_studio_name: str
) -> Studio:
    """Change studio's name."""

    studio = await get_by_name(Studio, studio_name, session)
    if not studio:
        raise DoesNotExist
    studio.name = new_studio_name
    await session.commit()
    return studio


async def delete_studio(session: AsyncSession, studio: Studio) -> str:
    "Delete the studio."

    await session.delete(studio)
    await session.commit()
    return studio.name


# Groups.
async def add_group(
        session: AsyncSession,
        group_name: str,
        studio_name: str,
        start_time: time,
        start_date: WeekDays
) -> Group:
    "Add a new group."

    if await get_by_name(Group, group_name, session):
        raise EntityAlreadyExists
    studio = await get_by_name(Studio, studio_name, session)
    if not studio:
        raise DoesNotExist
    group = Group(name=group_name, studio_id=studio.id)
    session.add(group)
    await session.flush()
    schedule = Schedule(
        group_id=group.id,
        start_time=start_time,
        start_date=start_date
    )
    session.add(schedule)
    await session.commit()


async def get_groups(session: AsyncSession, studio_name: str) -> list[Group]:
    "Get list of groups."

    studio = await get_by_name(Studio, studio_name, session)
    return studio.groups


async def edit_group(
        session: AsyncSession,
        group_name: str,
        new_group_name: str,
        studio_name: str
) -> Group:
    """Edit group."""

    studio = await get_by_name(Studio, studio_name, session)

    group = None
    for gr in studio.groups:
        if gr.name == group_name:
            group = gr

    if not group:
        raise DoesNotExist

    group.name = new_group_name
    await session.commit()
    return group


async def delete_group():
    pass


async def date_time_group():
    pass


async def edit_date_group():
    pass


async def edit_time_group():
    pass
