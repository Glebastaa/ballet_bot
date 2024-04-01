from contextlib import nullcontext as does_not_raise
from datetime import datetime

import pytest

from pydantic import ValidationError
from sqlalchemy import select

from database.models import Group, Schedule, Studio, WeekDays
from exceptions import EntityAlreadyExists, ScheduleTimeInsertionError
from schemas.constant import NAME_MAX_LENGTH, NAME_MIN_LENGTH
from schemas.group import GroupSchema
from services.group import GroupService

from notes import notes_test


@pytest.mark.group_service
class TestGroupService:
    async def _get_by_studio_id(self, session, studio_id):
        studio = await session.get(Studio, studio_id)
        return studio.groups

    async def _get_schedules_by_group_id(self, session, group_id):
        stmt = select(Schedule).where(Schedule.group_id == group_id)
        schedule = await session.execute(stmt)
        return schedule.scalars().all()

    @pytest.mark.parametrize(
            'studio_id, expectation',
            [
                [1, does_not_raise()],
                [2, does_not_raise()],
                [5, does_not_raise()]  # Not exists.
            ]
    )
    async def test_get_groups(self, create_db, groups, studio_id, expectation):
        with expectation:
            groups = await GroupService().get_groups(studio_id)
            if groups:
                assert len(groups) == 3
                assert groups[0].name == 'Коноха'
                assert not groups[0].is_individual
                assert groups[1].name == 'Киригакурэ'
                assert not groups[1].is_individual
            else:
                assert len(groups) == 0

    async def test_get_indivs(self, create_db, indivs):
        indivs = await GroupService().get_groups(1, True)

        assert len(indivs) == 3
        for indiv in indivs:
            assert indiv.is_individual
            assert indiv.name in ['indiv№1', 'indiv№2', 'indiv№3']

    @pytest.mark.parametrize(
            'studio_id, group_name, notes, expectation',
            [
                [1, '', notes_test, pytest.raises(ValidationError)],
                [1, None, notes_test, pytest.raises(ValidationError)],
                [1, 1, notes_test, pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MIN_LENGTH - 1),
                 notes_test, pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MAX_LENGTH + 1),
                 notes_test, pytest.raises(ValidationError)],
                [1, 'Анбу', notes_test, does_not_raise()],
                [1, 'Анбу', 123, pytest.raises(ValidationError)]
            ]
    )
    async def test_add_group(
        self,
        session,
        studios,
        studio_id,
        group_name,
        notes,
        expectation
    ):
        with expectation:
            await GroupService().add_group(group_name, studio_id, notes)

            group = await self._get_by_studio_id(session, studio_id)
            assert len(group) == 1
            assert group[0].name == group_name
            assert not group[0].is_individual

    async def test_add_indiv(self, session, indivs):
        test = await GroupService().add_group(
            'sdafafsd',
            1,
            is_individual=True
        )
        indiv = await session.get(Group, test.id)
        assert indiv is not None
        assert indiv.is_individual

        duplicate_group = await GroupService().add_group(
            'Коноха',
            1,
            is_individual=True
        )
        indiv_2 = await session.get(Group, duplicate_group.id)
        assert indiv_2 is not None
        assert indiv_2.name == 'Коноха'
        assert indiv_2.is_individual

    @pytest.mark.parametrize(
        'group_id, start_time, start_date, expectation',
        [
            [3, datetime.strptime('10:23', "%H:%M").time(),
             WeekDays.monday, does_not_raise()],
            [2, datetime.strptime('0:23', "%H:%M").time(),
             WeekDays.monday, does_not_raise()],
            [1, datetime.strptime('10:23', "%H:%M").time(),
             WeekDays.friday, does_not_raise()],
            [1, datetime.strptime('09:23', "%H:%M").time(),
             WeekDays.monday, does_not_raise()],
            [1, datetime.strptime('10:43', "%H:%M").time(),
             WeekDays.monday, pytest.raises(ScheduleTimeInsertionError)],
            [1, datetime.strptime('10:03', "%H:%M").time(),
             WeekDays.monday, pytest.raises(ScheduleTimeInsertionError)],
            [3, datetime.strptime('10:23', "%H:%M").time(),
             WeekDays('Четверг'), does_not_raise()]
        ])
    async def test_schedule_to_group(
        self,
        session,
        groups,
        group_id,
        start_time,
        start_date,
        expectation
    ):
        with expectation:
            await GroupService().add_schedule_to_group(
                group_id,
                start_time,
                start_date
            )
            schedules = await self._get_schedules_by_group_id(
                    session, group_id)
            for schedule in schedules:
                assert schedule is not None

    async def test_add_duplicate_in_same_studio(self, session, groups):
        with pytest.raises(EntityAlreadyExists):
            await GroupService().add_group('Коноха', 1)

    async def test_add_duplicate_in_another_studio(self, session, groups):
        await GroupService().add_group('Коноха', 2)

        group = await self._get_by_studio_id(session, 2)
        assert len(group) == 1
        assert group[0].name == 'Коноха'
        assert not group[0].is_individual

    @pytest.mark.parametrize(
            'group_id, group_name, notes, expectation',
            [
                [1, 'Анбу', None, does_not_raise()],
                [1, 'Анбу', notes_test, does_not_raise()],
                [1, 'Анбу', None, does_not_raise()],
                [1, '', None, pytest.raises(ValidationError)],
                [1, None, notes_test, does_not_raise()],
                [1, None, None, does_not_raise()],
                [1, 1, None, pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MIN_LENGTH - 1), None,
                 pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MAX_LENGTH + 1), None,
                 pytest.raises(ValidationError)],
                # Already exists.
                [1, 'Коноха', None, pytest.raises(EntityAlreadyExists)]
            ]
    )
    async def test_edit_group(
        self,
        session,
        groups,
        group_id,
        group_name,
        notes,
        expectation
    ):
        with expectation:
            old_group = (
                await session.get(Group, group_id)
            ).to_read_model(GroupSchema)
            await GroupService().edit_group(group_id, group_name, notes)
            new_group = (
                await session.get(Group, group_id)
            ).to_read_model(GroupSchema)

            if group_name:
                assert new_group.name == group_name
            else:
                assert new_group.name == old_group.name

            if notes:
                assert new_group.notes == notes
            else:
                assert new_group.notes == old_group.notes

    async def test_delete_group(self, session, indivs):
        name = await GroupService().delete_group(2)
        group = await session.get(Group, 2)
        assert group is None
        assert name == 'Киригакурэ'

        indiv_name = await GroupService().delete_group(4)
        indiv = await session.get(Group, 4)
        assert indiv is None
        assert indiv_name == 'indiv№1'

    async def test_get_date_time_group(self, session, groups):
        dt_list = await GroupService().get_date_time_group(1)

        for dt in dt_list:
            assert dt.start_time.strftime("%H:%M") == '10:23'
            assert dt.start_date.value == 'Понедельник'

    @pytest.mark.parametrize(
            'schedule_id, new_date, expectation',
            [
                [1, WeekDays.friday, does_not_raise()],
                [1, WeekDays.sunday, does_not_raise()],
                [5, WeekDays.sunday,
                 pytest.raises(ScheduleTimeInsertionError)],
            ]
    )
    async def test_edit_date_group(
        self,
        session,
        groups,
        schedule_id,
        new_date,
        expectation
    ):
        with expectation:
            old_schedule = await session.get(Schedule, schedule_id)
            old_date = old_schedule.start_date
            old_time = old_schedule.start_time
            await GroupService().edit_date_time_group(
                 schedule_id, new_date=new_date)

            schedule = await session.get(Schedule, schedule_id)
            await session.refresh(schedule)
            assert schedule.start_time == old_time
            assert schedule.start_date != old_date
            assert schedule.start_date == new_date

    @pytest.mark.parametrize(
            'schedule_id, new_time, expectation',
            [
                [1, datetime.strptime('10:43', "%H:%M").time(),
                 does_not_raise()],
                [2, datetime.strptime('10:43', "%H:%M").time(),
                 does_not_raise()],
                [4, datetime.strptime('10:43', "%H:%M").time(),
                 pytest.raises(ScheduleTimeInsertionError)],
            ]
    )
    async def test_edit_time_group(
        self,
        session,
        groups,
        schedule_id,
        new_time,
        expectation
    ):
        with expectation:
            old_schedule = await session.get(Schedule, schedule_id)
            old_date = old_schedule.start_date
            old_time = old_schedule.start_time

            await GroupService().edit_date_time_group(
                schedule_id,
                new_time=new_time
            )

            schedule = await session.get(Schedule, schedule_id)
            await session.refresh(schedule)
            assert schedule.start_date == old_date
            assert schedule.start_time != old_time
            assert schedule.start_time == new_time

    @pytest.mark.parametrize(
            'student_id, is_individual, gr_name, expectation',
            [
                [1, False, 'Коноха', does_not_raise()],
                [1, True, 'indiv№1', does_not_raise()]
            ]
    )
    async def test_get_groups_from_student(
        self,
        session,
        students_indivs,
        student_id,
        is_individual,
        gr_name,
        expectation
    ):
        with expectation:
            groups = await GroupService().get_groups_from_student(
                student_id, is_individual)

            assert len(groups) == 1
            assert groups[0].name == gr_name

    async def test_get_date_time_from_studion(
            self,
            session,
            indivs
    ):
        date_time = await GroupService().get_date_time_indivs_by_studio(1)
        assert isinstance(date_time, list)
        assert len(date_time) == 2
        assert date_time[0].start_date == WeekDays.monday
        assert date_time[1].start_date == WeekDays.friday

    async def test_delete_notes(self, session, groups):
        old_group = (await session.get(Group, 2)).to_read_model(GroupSchema)
        assert old_group.notes == notes_test
        await GroupService().delete_notes(2)

        group = await session.get(Group, 2)
        assert group.notes is None
        assert group.name == old_group.name
        assert group.is_individual == old_group.is_individual
        assert group.studio_id == old_group.studio_id

    @pytest.mark.parametrize(
            'group_id, expect',
            [
                [1, None],
                [2, notes_test]
            ]
    )
    async def test_get_notes(self, session, groups, group_id, expect):
        notes = await GroupService().get_notes(group_id)
        assert notes == expect

    async def test_delete_schedule(self, session, groups):
        await GroupService().delete_schedule(1)
        schedule = await session.get(Schedule, 1)
        assert schedule is None
