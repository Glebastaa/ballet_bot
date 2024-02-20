from sqlalchemy.ext.asyncio import AsyncSession

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

    student = await session.get(Student, student_id)
    group = await session.get(Group, group_id)
    student.groups.append(group)
    group.students.append(student)
    await session.commit()


async def get_students_from_group(
        session: AsyncSession,
        group_id: int
) -> list[Student]:
    """Get list of students from the group."""

    pass