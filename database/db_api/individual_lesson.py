from datetime import time

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import IndividualLesson, Student, WeekDays
from exceptions import DoesNotExist


async def add_individual_lesson(
        session: AsyncSession,
        studio_id: int,
        start_time: time,
        start_date: WeekDays,
        notes: str | None = None
) -> IndividualLesson:
    """Add new individual lesson."""

    new_lesson = IndividualLesson(
        start_time=start_time,
        start_date=start_date,
        studio_id=studio_id,
        notes=notes
    )
    session.add(new_lesson)
    await session.commit()


async def get_date_time_individual_lesson(
        session: AsyncSession,
        indiv_id: int
) -> list[time, WeekDays]:
    """Get start_time, start_date from a individual lesson."""

    lesson = await session.get(IndividualLesson, indiv_id)
    if not lesson:
        raise DoesNotExist
    return [lesson.start_time, lesson.start_date]


async def delete_individual_lesson(
        session: AsyncSession,
        indiv_id: int
) -> None:
    """Delete individual lesson."""

    indiv = await session.get(IndividualLesson, 1)
    await session.delete(indiv)
    await session.commit()


async def add_student_to_individual_lesson(
        session: AsyncSession,
        indiv_id: int,
        student_id: int
) -> None:
    """Add a student to individual lesson."""

    student = await session.get(Student, student_id)
    student.individual_lesson_id = indiv_id
    await session.commit()
