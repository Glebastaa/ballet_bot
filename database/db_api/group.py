from datetime import time

from sqlalchemy.ext.asyncio import AsyncSession
from database.db_api.utils import get_schedule, group_not_in_studio

from database.models import Group, Schedule, Studio, WeekDays
from exceptions import EntityAlreadyExists


async def add_group(
        session: AsyncSession,
        group_name: str,
        studio_id: int,
        start_time: time,
        start_date: WeekDays
) -> Group:
    "Add a new group."

    if await group_not_in_studio(session, group_name, studio_id):
        raise EntityAlreadyExists
    studio = await session.get(Studio, studio_id)
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


async def get_groups(session: AsyncSession, studio_id: int) -> list[Group]:
    "Get list of groups."

    studio = await session.get(Studio, studio_id)
    return studio.groups


async def edit_group(
        session: AsyncSession,
        group_id: int,
        new_group_name: str
) -> Group:
    """Edit group."""

    group = await session.get(Group, group_id)
    group.name = new_group_name
    await session.commit()
    return group


async def delete_group(
        session: AsyncSession,
        group_id: int
) -> str:
    """Delete group."""

    group = await session.get(Group, group_id)
    await session.delete(group)
    await session.commit()
    return group.name


async def get_date_time_group(
        session: AsyncSession,
        group_id: int
):
    """Get datetime."""

    group = await session.get(Group, group_id)
    schedule = await get_schedule(session, group)
    return [schedule.start_date.value, schedule.start_time.strftime('%H:%M')]


async def edit_date_group(
        session: AsyncSession,
        group_id: int,
        new_date: WeekDays
) -> Schedule:
    """Edit date."""

    group = await session.get(Group, group_id)
    schedule = await get_schedule(session, group)
    schedule.start_date = new_date
    await session.commit()
    return schedule


async def edit_time_group(
        session: AsyncSession,
        group_id: int,
        new_time: time
) -> Schedule:
    """Edit time."""

    group = await session.get(Group, group_id)
    schedule = await get_schedule(session, group)
    schedule.start_time = new_time
    await session.commit()
    return schedule
