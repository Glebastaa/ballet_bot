from datetime import time

from sqlalchemy.ext.asyncio import AsyncSession
from database.db_api.utils import get_by_name, get_group_by_name_and_studio, get_schedule

from database.models import Group, Schedule, Studio, WeekDays
from exceptions import DoesNotExist, EntityAlreadyExists


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
    if not studio:
        raise DoesNotExist
    return studio.groups


async def edit_group(
        session: AsyncSession,
        group_name: str,
        new_group_name: str,
        studio_name: str
) -> Group:
    """Edit group."""

    group = await get_group_by_name_and_studio(
        session,
        group_name,
        studio_name
    )
    group.name = new_group_name
    await session.commit()
    return group


async def delete_group(
        session: AsyncSession,
        group_name: str,
        studio_name: str
) -> str:
    """Delete group."""

    group = await get_group_by_name_and_studio(
        session,
        group_name,
        studio_name
    )
    await session.delete(group)
    await session.commit()
    return group_name


async def get_date_time_group(
        session: AsyncSession,
        group_name: str,
        studio_name: str
):
    """Get datetime."""

    group = await get_group_by_name_and_studio(
        session,
        group_name,
        studio_name
    )
    schedule = await get_schedule(session, group)
    return [schedule.start_date.value, schedule.start_time.strftime('%H:%M')]


async def edit_date_group(
        session: AsyncSession,
        group_name: str,
        studio_name: str,
        new_date: WeekDays
) -> Schedule:
    """Edit date."""

    group = await get_group_by_name_and_studio(
        session,
        group_name,
        studio_name
    )
    schedule = await get_schedule(session, group)
    schedule.start_date = new_date
    await session.commit()
    return schedule


async def edit_time_group(
        session: AsyncSession,
        group_name: str,
        studio_name: str,
        new_time: time
) -> Schedule:
    """Edit time."""

    group = await get_group_by_name_and_studio(
        session,
        group_name,
        studio_name
    )
    schedule = await get_schedule(session, group)
    schedule.start_time = new_time
    await session.commit()
    return schedule