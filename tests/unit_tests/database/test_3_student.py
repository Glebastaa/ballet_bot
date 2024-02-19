from sqlalchemy import select

from database.db_api.student import add_student
from database.models import Student


class TestStudent:
    async def test_add_student(self, session, student_name):
        await add_student(session, student_name)

        stmt = select(Student).where(Student.name == student_name)
        student = await session.execute(stmt)
        assert student.scalar_one_or_none().name == student_name
