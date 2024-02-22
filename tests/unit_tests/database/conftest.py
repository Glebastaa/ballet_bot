from datetime import datetime
import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models import (
    Group,
    IndividualLesson,
    Schedule,
    Student,
    Studio,
    WeekDays
)


# Studio.

@pytest.fixture
async def studios(session):
    studio_1 = Studio(name='Страна огня')
    studio_2 = Studio(name='Страна воды')
    studio_3 = Studio(name='Страна ветра')
    session.add_all([studio_1, studio_2, studio_3])
    await session.commit()


# Group.

@pytest.fixture
async def groups(session, studios):
    group_1 = Group(
        name='Коноха',
        studio_id=1,
        notes=None
    )
    group_2 = Group(
        name='Киригакурэ',
        studio_id=1,
        notes=None
    )
    schedule_1 = Schedule(
        group_id=1,
        start_time=datetime.strptime('10:23', "%H:%M").time(),
        start_date=WeekDays.monday
    )
    schedule_2 = Schedule(
        group_id=2,
        start_time=datetime.strptime('16:43', "%H:%M").time(),
        start_date=WeekDays.friday
    )
    session.add_all([group_1, group_2, schedule_1, schedule_2])
    await session.commit()


# Student.

@pytest.fixture
async def students(session):
    student_1 = Student(
        name='Наруто',
        notes=None,
        individual_lesson_id=None
    )
    student_2 = Student(
        name='Саске',
        notes=None,
        individual_lesson_id=None
    )
    student_3 = Student(
        name='Сакура',
        notes=None,
        individual_lesson_id=None
    )
    session.add_all([student_1, student_2, student_3])
    await session.commit()


# For association table.
@pytest.fixture
async def students_groups(session, students, groups):
    students = await session.execute(select(Student))
    stmt = select(Group).where(Group.id == 1).options(
        selectinload(Group.students))
    group = await session.scalar(stmt)

    group.students = students.scalars().all()
    await session.commit()


# Indiv lesson.

@pytest.fixture
async def indivs(session, studios):
    indiv_1 = IndividualLesson(
        start_time=datetime.strptime('11:11', "%H:%M").time(),
        start_date=WeekDays.monday,
        notes=None,
        studio_id=1
    )
    indiv_2 = IndividualLesson(
        start_time=datetime.strptime('22:22', "%H:%M").time(),
        start_date=WeekDays.tuesday,
        notes=None,
        studio_id=1
    )
    indiv_3 = IndividualLesson(
        start_time=datetime.strptime('23:33', "%H:%M").time(),
        start_date=WeekDays.wednesday,
        notes=None,
        studio_id=1
    )
    session.add_all([indiv_1, indiv_2, indiv_3])
    await session.commit()
