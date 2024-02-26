from datetime import time
from database.models import WeekDays
from exceptions import DoesNotExist
from schemas.individual_lesson import IndivSchema, IndivSchemaAdd
from utils.unitofwork import UnitOfWork


class IndividualLessonService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def add_individual_lesson(
        self,
        studio_id: int,
        start_time: time,
        start_date: WeekDays,
        notes: str | None = None
    ) -> IndivSchema:
        """Add new individual lesson."""
        validated_data = IndivSchemaAdd(
            start_time=start_time,
            start_date=start_date,
            studio_id=studio_id,
            notes=notes
        )
        async with self.uow:
            indiv = await self.uow.individual_lesson.add(
                validated_data.model_dump()
            )
            await self.uow.commit()
            return indiv

    async def get_date_time_from_indiv(
            self,
            indiv_id: int
    ) -> list[time, WeekDays]:
        """Get start_time, start_date from a individual lesson."""
        async with self.uow:
            lesson = await self.uow.individual_lesson.get(indiv_id)
            if not lesson:
                raise DoesNotExist
            return [lesson.start_time, lesson.start_date]

    async def delete_individual_lesson(
            self,
            indiv_id: int
    ) -> str:
        """Delete individual lesson."""
        async with self.uow:
            lesson = await self.uow.individual_lesson.delete(indiv_id)
            studio = await self.uow.studio.get(id=lesson.studio_id)
            await self.uow.commit()
            return studio.name

    async def add_student_to_individual_lesson(
            self,
            indiv_id: int,
            student_id: int
    ) -> None:
        """Add a student to individual lesson."""
        async with self.uow:
            indiv = await self.uow.individual_lesson.get(indiv_id)
            student = await self.uow.student.get(student_id)
            await self.uow.session.refresh(indiv, attribute_names=['students'])
            indiv.students.append(student)
            await self.uow.commit()
