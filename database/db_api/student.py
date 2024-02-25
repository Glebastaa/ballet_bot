from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import Group, Student


async def add_student(session: AsyncSession, student_name: str) -> Student:
    """Create new student in db."""

    student = Student(name=student_name)
    session.add(student)
    await session.commit()
    return student


async def add_student_to_group(
        session: AsyncSession,
        student_id: int,
        group_id: int
) -> None:
    """Add student to group."""

    student = await session.scalar(
        select(Student).where(Student.id == student_id)
    )
    group = await session.scalar(
        select(Group).where(
            Group.id == group_id).options(selectinload(Group.students))
        )
    group.students.append(student)
    await session.commit()


async def get_students_from_group(
        session: AsyncSession,
        group_id: int
) -> list[Student | None]:
    """Get list of students from the group."""

    stmt = select(Group).where(Group.id == group_id).options(
        selectinload(Group.students))
    group = await session.scalar(stmt)
    return group.students


async def edit_student(
        session: AsyncSession,
        student_id: int,
        new_name: str
) -> Student:
    """Edit student's name."""

    student = await session.get(Student, student_id)
    student.name = new_name
    await session.commit()
    return student


async def delete_student(
        session: AsyncSession,
        student_id: int
) -> str:
    """Delete a student."""

    student = await session.get(Student, student_id)
    await session.delete(student)
    await session.commit()
    return student.name
