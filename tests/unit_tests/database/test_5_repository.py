import pytest

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models import Group, IndividualLesson, Schedule, Student, Studio, WeekDays
from exceptions import DoesNotExist, EntityAlreadyExists
from services.group import GroupService
from services.individual_lesson import IndividualLessonService
from services.student import StudentService
from services.studio import StudioService


@pytest.mark.repo
class TestServiceStudio:
    async def test_serv_add_studio(self, session):
        name = 'Акихабара'
        studio = await StudioService().add_studio(name)
        assert studio.name == 'Акихабара'

    async def test_serv_get_studios(self, session, studios):
        studios = await StudioService().get_studios()

        assert studios is not None
        assert len(studios) == 3
        assert set(
            [studio.name for studio in studios]
        ) == set(['Страна огня', 'Страна воды', 'Страна ветра'])

    async def test_edit_studios(self, session, studios):
        await StudioService().edit_studio(1, 'Яметте кудасай, ониии-чан!')
        studio = await session.scalar(select(Studio).where(Studio.id == 1))
        assert studio.name == 'Яметте кудасай, ониии-чан!'

    async def test_delete_studio(self, session, studios):
        old_studio = await session.get(Studio, 1)
        old_name = old_studio.name
        await StudioService().delete_studio(1)

        studio = await session.scalar(select(Studio).where(Studio.id == 1))
        assert studio is None
        assert old_name == 'Страна огня'


@pytest.mark.repo2
class TestServiceGroup:
    async def _get_by_studio_id(self, session, studio_id):
        studio = await session.get(Studio, studio_id)
        return studio.groups

    async def _get_schedule_by_group_id(self, session, group_id):
        stmt = select(Schedule).where(Schedule.group_id == group_id)
        schedule = await session.execute(stmt)
        return schedule.scalar_one_or_none()

    async def test_get_groups(self, create_db, groups):
        groups = await GroupService().get_groups(1)
        assert len(groups) == 2
        assert groups[0].name == 'Коноха'
        assert groups[1].name == 'Киригакурэ'

    @pytest.mark.parametrize(
        'data',
        [
            ['Анбу', 1],
            ['Анбу', 1, datetime.strptime('10:23', "%H:%M").time(),
             WeekDays.monday],
            ['Анбу', 1, datetime.strptime('10:23', "%H:%M").time(),
             'Понедельник'],
            # ['Анбу', 1, datetime.strptime('10:23', "%H:%M").time(),
            #  'Выдуманный день']
        ])
    async def test_add_group(self, session, studios, data):
        await GroupService().add_group(*data)

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
            await GroupService().add_group('Коноха', 1)

    async def test_add_duplicate_in_another_studio(self, session, groups):
        await GroupService().add_group('Коноха', 2)

        group = await self._get_by_studio_id(session, 2)
        assert len(group) == 1
        assert group[0].name == 'Коноха'

    async def test_edit_group(self, session, groups):
        old = await GroupService().edit_group(2, 'Анбу')
        old_notes = old.notes

        edited_group = await session.get(Group, 2)
        assert edited_group.name == 'Анбу'
        assert edited_group.notes == old_notes

    async def test_delete_group(self, session, groups):
        name = await GroupService().delete_group(2)
        group = await session.get(Group, 2)
        assert group is None
        assert name == 'Киригакурэ'

    async def test_get_date_time_group(self, session, groups):
        dt_list = await GroupService().get_date_time_group(1)

        for dt in dt_list:
            assert dt[0] == '10:23'
            assert dt[1] == 'Понедельник'

    async def test_edit_date_group(self, session, groups):
        old_schedule = await session.get(Schedule, 1)
        old_date = old_schedule.start_date
        old_time = old_schedule.start_time
        await GroupService().edit_date_time_group(1, new_date=WeekDays.sunday)

        schedule = await session.get(Schedule, 1)
        await session.refresh(schedule)
        assert schedule.start_time == old_time
        assert schedule.start_date != old_date
        assert schedule.start_date == WeekDays.sunday

    async def test_edit_time_group(self, session, groups):
        old_schedule = await session.get(Schedule, 1)
        old_date = old_schedule.start_date
        old_time = old_schedule.start_time

        await GroupService().edit_date_time_group(
            1,
            new_time=datetime.strptime('11:11', "%H:%M").time()
        )

        schedule = await session.get(Schedule, 1)
        await session.refresh(schedule)
        assert schedule.start_date == old_date
        assert schedule.start_time != old_time
        assert schedule.start_time.strftime('%H:%M') == '11:11'


@pytest.mark.repo3
class TestStudentService:
    async def test_add_student(self, session):
        await StudentService().add_student('Конохамару')

        student = await session.execute(select(Student))
        student = student.scalars().all()
        assert len(student) == 1
        assert student[0].name == 'Конохамару'

    async def test_add_student_to_group(self, session, groups, students):
        await StudentService().add_student_to_group(1, 1)

        stmt = select(Group).where(Group.id == 1).options(
            selectinload(Group.students))

        group = await session.scalar(stmt)
        students = group.students
        assert students[0].name == 'Наруто'
        assert group.name == 'Коноха'

    async def test_get_students_from_group(self, session, students_groups):
        students = await StudentService().get_students_from_group(1)
        students_2 = await StudentService().get_students_from_group(2)

        assert students is not None
        assert len(students) == 3
        assert set(
            [student.name for student in students]
        ) == set(['Саске', 'Сакура', 'Наруто'])

        assert not students_2

    async def test_delete_student_from_group(self, session, students_groups):
        name = await StudentService().delete_student_from_group(1, 1)

        stmt = select(Group).where(Group.id == 1).options(
            selectinload(Group.students))
        group = await session.scalar(stmt)
        assert set(
            [student.name for student in group.students]
        ) == set(['Саске', 'Сакура'])
        assert name == 'Наруто'

    async def test_edit_student_name(self, session, students):
        old_name = (await session.get(Student, 1)).name
        await StudentService().edit_student(1, 'Уи-чан')

        new_student = await session.get(Student, 1)
        assert new_student.name == 'Уи-чан'
        assert old_name != new_student.name

    async def test_delete_student(self, session, students_groups):
        await StudentService().delete_student(1)

        student = await session.get(Student, 1)
        assert student is None

        stmt = select(Group).where(Group.id == 1).options(
            selectinload(Group.students)
        )
        group = await session.scalar(stmt)
        for st in group.students:
            assert st.id != 1

    async def test_get_all_students(self, students):
        students = await StudentService().get_all_students()

        assert set(
            [student.name for student in students]
        ) == set(['Саске', 'Сакура', 'Наруто'])


@pytest.mark.repo4
class TestIndividualLesson:
    async def _get_by_studio_id_or_all(self, session, studio_id: int = None):
        stmt = select(IndividualLesson)
        if studio_id:
            stmt = stmt.where(IndividualLesson.studio_id == studio_id)
        return await session.scalars(stmt)

    async def test_add_indiv_lesson(self, session, studios):
        await IndividualLessonService().add_individual_lesson(
            1,
            datetime.strptime('11:11', "%H:%M").time(),
            WeekDays.monday
        )

        indiv = await self._get_by_studio_id_or_all(session, 1)
        indiv = indiv.all()
        assert len(indiv) == 1
        assert indiv[0] is not None
        assert indiv[0].start_date == WeekDays.monday
        assert indiv[0].start_time.strftime("%H:%M") == '11:11'

    async def test_get_time_and_date_from_indiv(self, session, indivs):
        lesson = await IndividualLessonService().get_date_time_from_indiv(1)

        assert lesson is not None
        assert lesson[1] == WeekDays.monday
        assert lesson[0].strftime("%H:%M") == '11:11'\

        with pytest.raises(DoesNotExist):
            await IndividualLessonService().get_date_time_from_indiv(4)

    async def test_delete_individual_lesson(self, session, indivs):
        await IndividualLessonService().delete_individual_lesson(1)

        indiv = await session.get(IndividualLesson, 1)
        assert indiv is None

    # async def test_add_student_to_individual_lesson(
    #         self,
    #         session,
    #         indivs,
    #         students):
    #     await add_student_to_individual_lesson(session, 1, 1)

    #     stmt = select(IndividualLesson).where(
    #         IndividualLesson.id == 1).options(
    #             selectinload(IndividualLesson.students))
    #     indiv = await session.scalar(stmt)
    #     assert 1 == indiv.students[0].id
