from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Student


async def add_student(session: AsyncSession, student_name: str, age: int) -> Student:
    pass


async def get_students_from_group(session: AsyncSession, group_id: int) -> list[Student]:
    """Get list of students from the group."""

    stmt = select(Student).where(Student.group == group_id)