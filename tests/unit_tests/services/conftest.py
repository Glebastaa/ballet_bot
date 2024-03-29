from datetime import datetime

import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import (
    Group,
    Schedule,
    Student,
    Studio,
    User,
    UserRoles,
    WeekDays
)

from notes import notes_test


# Studio.

@pytest.fixture
async def studios(session: AsyncSession):
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
        notes=None,
        is_individual=False
    )
    group_2 = Group(
        name='Киригакурэ',
        studio_id=1,
        notes=notes_test,
        is_individual=False
    )
    group_3 = Group(
        name='Логово Орочимару',
        studio_id=1,
        notes=None,
        is_individual=False
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
    schedule_3 = Schedule(
        group_id=2,
        start_time=datetime.strptime('10:43', "%H:%M").time(),
        start_date=WeekDays.sunday
    )
    schedule_4 = Schedule(
        group_id=2,
        start_time=datetime.strptime('18:43', "%H:%M").time(),
        start_date=WeekDays.monday
    )
    schedule_5 = Schedule(
        group_id=2,
        start_time=datetime.strptime('10:43', "%H:%M").time(),
        start_date=WeekDays.monday
    )
    session.add_all(
        [group_1, group_2, group_3,
         schedule_1, schedule_2, schedule_3, schedule_4, schedule_5]
    )
    await session.commit()


@pytest.fixture
async def indivs(session, groups):
    indiv_1 = Group(
        name='indiv№1',
        studio_id=1,
        notes=None,
        is_individual=True
    )
    indiv_2 = Group(
        name='indiv№2',
        studio_id=1,
        notes=None,
        is_individual=True
    )
    indiv_3 = Group(
        name='indiv№3',
        studio_id=1,
        notes=None,
        is_individual=True
    )
    schedule_6 = Schedule(
        group_id=4,
        start_time=datetime.strptime('8:00', "%H:%M").time(),
        start_date=WeekDays.monday
    )
    schedule_7 = Schedule(
        group_id=5,
        start_time=datetime.strptime('19:00', "%H:%M").time(),
        start_date=WeekDays.friday
    )
    session.add_all([indiv_1, indiv_2, indiv_3, schedule_6, schedule_7])
    await session.commit()

# Student.


@pytest.fixture
async def students(session):
    student_1 = Student(
        name='Наруто',
        notes=None
    )
    student_2 = Student(
        name='Саске',
        notes=None
    )
    student_3 = Student(
        name='Сакура',
        notes=None
    )
    session.add_all([student_1, student_2, student_3])
    await session.commit()


# For association table.
@pytest.fixture
async def students_groups(session, students, indivs):
    students = await session.execute(select(Student))
    stmt = select(Group).where(Group.id == 1).options(
        selectinload(Group.students))
    group = await session.scalar(stmt)

    group.students = students.scalars().all()
    await session.commit()


@pytest.fixture
async def students_indivs(session, students_groups):
    student_1 = await session.get(Student, 1)
    student_2 = await session.get(Student, 2)
    stmt = select(Group).where(Group.id == 4).options(
        selectinload(Group.students))
    group = await session.scalar(stmt)

    group.students.append(student_1)
    group.students.append(student_2)
    await session.commit()


# User.
@pytest.fixture
async def users(session):
    user_1 = User(
        id=5213573061,
        username='Сасуми Хиросава',
        role=UserRoles.OWNER
    )
    user_2 = User(
        id=5223573061,
        username='Джо Хисаиши',
        role=UserRoles.TEACHER
    )
    user_3 = User(
        id=5233573061,
        username='Юрима',
        role=UserRoles.STUDENT
    )
    user_4 = User(
        id=5243573061,
        username='Tommy heavenly6',
        role=UserRoles.STUDENT
    )
    user_5 = User(
        id=5253573061,
        username='Aiobahn',
        role=UserRoles.VISITOR
    )
    user_6 = User(
        id=5263573061,
        username='Flow',
        role=UserRoles.VISITOR
    )
    session.add_all([user_1, user_2, user_3, user_4, user_5, user_6])
    await session.commit()
