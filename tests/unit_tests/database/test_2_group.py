from datetime import datetime
import pytest
from sqlalchemy import select

from database.db_api.group import (
    add_group,
    delete_group,
    edit_date_group,
    edit_group,
    edit_time_group,
    get_date_time_group,
    get_groups
)
from database.models import Group, Schedule, Studio, WeekDays
from exceptions import EntityAlreadyExists


@pytest.mark.group
class TestGroup:
    async def _get_by_studio_id(self, session, studio_id):
        studio = await session.get(Studio, studio_id)
        return studio.groups

    async def _get_schedule_by_group_id(self, session, group_id):
        stmt = select(Schedule).where(Schedule.group_id == group_id)
        schedule = await session.execute(stmt)
        return schedule.scalar_one_or_none()

    async def test_get_groups(self, session, groups):
        groups = await get_groups(session, 1)

        assert len(groups) == 2

    @pytest.mark.parametrize(
        'data',
        [
            ['Анбу', 1],
            ['Анбу', 1, datetime.strptime('10:23', "%H:%M").time(),
             WeekDays.monday]
        ])
    async def test_add_group(self, session, studios, data):
        await add_group(session, *data)

        group = await self._get_by_studio_id(session, 1)
        assert len(group) == 1
        assert group[0].name == 'Анбу'

        schedule = await self._get_schedule_by_group_id(
                session, group[0].id)
        if len(data) == 2:
            assert schedule is None
        else:
            assert schedule is not None
            assert schedule.start_date.value == 'Понедельник'
            assert schedule.start_time.strftime("%H:%M") == '10:23'

    async def test_add_duplicate_in_same_studio(self, session, groups):
        with pytest.raises(EntityAlreadyExists):
            await add_group(session, 'Коноха', 1)

    async def test_add_duplicate_in_another_studio(self, session, groups):
        await add_group(session, 'Коноха', 2)

        group = await self._get_by_studio_id(session, 2)
        assert len(group) == 1
        assert group[0].name == 'Коноха'

    async def test_edit_group(self, session, groups):
        await edit_group(session, 2, 'Анбу')

        edited_group = await session.get(Group, 2)
        assert edited_group.name == 'Анбу'

    async def test_delete_group(self, session, groups):
        await delete_group(session, 2)
        group = await session.get(Group, 2)
        assert group is None

    async def test_get_date_time_group(self, session, groups):
        dt = await get_date_time_group(session, 1)

        assert dt[0] == 'Понедельник'
        assert dt[1] == '10:23'

    async def test_edit_date_group(self, session, groups):
        old_schedule = await self._get_schedule_by_group_id(session, 1)
        old_date = old_schedule.start_date
        old_time = old_schedule.start_time
        await edit_date_group(session, 1, WeekDays.sunday)

        schedule = await self._get_schedule_by_group_id(session, 1)
        assert schedule.start_time == old_time
        assert schedule.start_date != old_date
        assert schedule.start_date == WeekDays.sunday

    async def test_edit_time_group(self, session, groups):
        old_schedule = await self._get_schedule_by_group_id(session, 1)
        old_date = old_schedule.start_date
        old_time = old_schedule.start_time

        await edit_time_group(
            session,
            1,
            datetime.strptime('11:11', "%H:%M").time()
        )

        schedule = await self._get_schedule_by_group_id(session, 1)
        assert schedule.start_date == old_date
        assert schedule.start_time != old_time
        assert schedule.start_time.strftime('%H:%M') == '11:11'
