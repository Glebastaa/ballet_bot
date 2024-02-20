import pytest
from sqlalchemy import select

from database.db_api.group import add_group, delete_group, edit_group, get_groups
from database.models import Group, Schedule, Studio
from exceptions import EntityAlreadyExists


class TestGroup:
    async def _get_by_studio_id(self, session, studio_id):
        studio = await session.get(Studio, studio_id)
        return studio.groups

    async def _get_schedule_by_group_id(self, session, group_id: int = None):
        stmt = select(Schedule).where(Schedule.group_id == group_id)
        schedule = await session.execute(stmt)
        return schedule.scalar_one_or_none()

    async def test_add_groups(self, session, first_group, second_group):
        await add_group(session, *first_group.values())
        await add_group(session, *second_group.values())

        groups = await self._get_by_studio_id(
            session,
            first_group['studio_id']
        )
        assert groups[0].name == first_group['name']
        assert groups[1].name == second_group['name']

        schedule = await self._get_schedule_by_group_id(session, groups[0].id)
        assert schedule is not None
        assert schedule.start_time == first_group['time']
        assert schedule.start_date == first_group['date']

    async def test_add_duplicate_in_same_studio(self, session, first_group):
        with pytest.raises(EntityAlreadyExists):
            await add_group(session, *first_group.values())

    async def test_add_duplicate_in_another_studio(self, session, first_group):
        data = first_group
        data['studio_id'] = 3
        await add_group(session, *data.values())

        group = await self._get_by_studio_id(session, data['studio_id'])
        assert len(group) > 0
        assert group[0].name == first_group['name']

    async def test_get_groups(self, session, first_group, second_group):
        groups = await get_groups(session, first_group['studio_id'])

        assert len(groups) == 2
        assert groups[0].name == first_group['name']
        assert groups[1].name == second_group['name']

    async def test_edit_group(self, session):
        old_group = await session.get(Group, 2)
        await edit_group(session, 2, 'Анбу')

        group = await session.get(Group, 2)
        assert group.name == 'Анбу'
        assert group.notes == old_group.notes
        assert group.studio_id == old_group.studio_id

    async def test_delete_group(self, session):
        await delete_group(session, 2)
        group = await session.get(Group, 2)
        assert group is None
