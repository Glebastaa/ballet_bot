import pytest

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.db_api.student import add_student, delete_student, edit_student, get_students_from_group
from database.models import Group, Student


@pytest.mark.student
class TestStudent:
    async def test_add_student(self, session):
        await add_student(session, 'Конохамару')

        student = await session.execute(select(Student))
        student = student.scalars().all()
        assert len(student) == 1
        assert student[0].name == 'Конохамару'

    async def test_get_students_from_group(self, session, students_groups):
        students = await get_students_from_group(session, 1)
        students_2 = await get_students_from_group(session, 2)

        assert students is not None
        assert len(students) == 3
        assert set(
            [student.name for student in students]
        ) == set(['Саске', 'Сакура', 'Наруто'])

        assert not students_2

    async def test_edit_student_name(self, session, students):
        old_name = (await session.get(Student, 1)).name
        await edit_student(session, 1, 'Уи-чан')

        new_student = await session.get(Student, 1)
        assert new_student.name == 'Уи-чан'
        assert old_name != new_student.name

    async def test_delete_student(self, session, students_groups):
        await delete_student(session, 1)

        student = await session.get(Student, 1)
        assert student is None

        stmt = select(Group).where(Group.id == 1).options(
            selectinload(Group.students)
        )
        group = await session.scalar(stmt)
        for st in group.students:
            assert st.id != 1
