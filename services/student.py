from exceptions import (
    IndivIsFull,
    InvalidIsIndividual,
    StudentAlreadyInGroupError
)
from logger_config import setup_logger
from schemas.constant import MAX_STUDENTS_IN_INDIV
from schemas.student import (
    StudentNotesSchema,
    StudentSchema,
    StudentSchemaAdd,
    StudentSchemaUpdate
)
from utils.unitofwork import UnitOfWork


logger = setup_logger('student')


class StudentService:
    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    async def add_student(self, student_name: str) -> StudentSchema:
        """Create a new student in db."""
        validated_data = StudentSchemaAdd(name=student_name)
        async with self.uow:
            student = await self.uow.student.add(
                validated_data.model_dump()
            )
            await self.uow.commit()
            logger.info(f'Ученик "{student_name}" добавлен.')
            return student.to_read_model(StudentSchema)

    async def add_student_to_group(
            self,
            student_id: int,
            group_id: int,
            is_individual: bool = False
    ) -> None:
        """Add a student to group."""
        async with self.uow:
            student = await self.uow.student.get(id=student_id)
            group = await self.uow.group.get(id=group_id)

            # if try add to group with is_individual=True or vice versa.
            if group.is_individual != is_individual:
                raise InvalidIsIndividual

            await self.uow.session.refresh(group, attribute_names=['students'])
            if student in group.students:
                raise StudentAlreadyInGroupError({'student_id': student.id})
            if is_individual and len(group.students) >= MAX_STUDENTS_IN_INDIV:
                raise IndivIsFull({'group_id': group.id})
            group.students.append(student)
            await self.uow.commit()
            logger.info(
                f'Ученик "{student.name}" добавлен в группу "{group.name}".'
            )

    async def get_students_from_group(
            self,
            group_id: int
    ) -> list[StudentSchema]:
        """Gets list of students from the group."""
        async with self.uow:
            group = await self.uow.group.get(id=group_id)
            await self.uow.session.refresh(group, attribute_names=['students'])
            return [st.to_read_model(StudentSchema) for st in group.students]

    async def get_all_students(
            self
    ) -> list[StudentSchema]:
        """Gets list of all students from the db."""
        async with self.uow:
            students = await self.uow.student.get_all()
            return [st.to_read_model(StudentSchema) for st in students]

    async def delete_student_from_group(
            self,
            student_id: int,
            group_id: int
    ) -> str:
        """Delete a student from group."""
        async with self.uow:
            student = await self.uow.student.get(id=student_id)
            group = await self.uow.group.get(id=group_id)
            await self.uow.session.refresh(group, attribute_names=['students'])
            group.students.remove(student)
            await self.uow.commit()
            logger.info(
                f'Ученик "{student.name}" удален из группы "{group.name}".'
            )
            return student.name

    async def edit_student(
            self,
            student_id: int,
            new_name: str
    ) -> StudentSchema:
        """Edit a student's name."""
        validated_data = StudentSchemaUpdate(name=new_name)
        async with self.uow:
            student = await self.uow.student.update(
                data=validated_data.model_dump(exclude_none=True),
                id=student_id
            )
            await self.uow.commit()
            logger.info(
                f'У ученика по id: {student_id} изменено имя на "{new_name}"')
            return student.to_read_model(StudentSchema)

    async def delete_student(
            self,
            student_id: int
    ) -> str:
        """Delete a student."""
        async with self.uow:
            student = await self.uow.student.delete(id=student_id)
            await self.uow.commit()
            logger.info(f'Ученик "{student.name}" удален.')
            return student.name

    async def edit_or_delete_notes(
            self,
            student_id: int,
            notes: str | None
    ) -> str | None:
        """Edit or delete notes by student id."""
        async with self.uow:
            data = StudentNotesSchema(notes=notes)
            student = await self.uow.student.update(
                data.model_dump(), id=student_id)
            await self.uow.commit()
            return student.notes

    async def get_notes(self, student_id: int) -> str | None:
        """Get notes from student."""
        async with self.uow:
            student = await self.uow.student.get(id=student_id)
            return student.notes
