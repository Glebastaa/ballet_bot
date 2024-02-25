from schemas.student import StudentSchema, StudentSchemaAdd, StudentSchemaUpdate
from utils.unitofwork import UnitOfWork


class StudentService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def add_student(self, student_name: str) -> StudentSchema:
        """Create new student in db."""
        validated_data = StudentSchemaAdd(name=student_name)
        async with self.uow:
            student = await self.uow.student.add(
                validated_data.model_dump()
            )
            await self.uow.commit()
            return student.to_read_model(StudentSchema)

    async def add_student_to_group(
            self,
            student_id: int,
            group_id: int
    ) -> None:
        """Add student to group."""
        async with self.uow:
            student = await self.uow.student.get(student_id)
            group = await self.uow.group.get(group_id)
            await self.uow.session.refresh(group, attribute_names=['students'])
            group.students.append(student)
            await self.uow.commit()

    async def get_students_from_group(
            self,
            group_id: int
    ) -> list[StudentSchema | None]:
        """Get list of students from the group."""
        async with self.uow:
            group = await self.uow.group.get(group_id)
            await self.uow.session.refresh(group, attribute_names=['students'])
            return [st.to_read_model(StudentSchema) for st in group.students]

    async def delete_student_from_group(
            self,
            student_id: int,
            group_id: int
    ) -> str:
        """Delete a student from group."""
        async with self.uow:
            student = await self.uow.student.get(student_id)
            group = await self.uow.group.get(group_id)
            await self.uow.session.refresh(group, attribute_names=['students'])
            group.students.remove(student)
            await self.uow.commit()
            return student.name

    async def edit_student(
            self,
            student_id: int,
            new_name: str
    ) -> StudentSchema:
        """Edit student's name."""
        validated_data = StudentSchemaUpdate(name=new_name)
        async with self.uow:
            student = await self.uow.student.update(
                student_id,
                validated_data.model_dump(exclude_none=True)
            )
            await self.uow.commit()
            return student

    async def delete_student(
            self,
            student_id: int
    ) -> str:
        """Delete a student."""
        async with self.uow:
            student = await self.uow.student.delete(student_id)
            await self.uow.commit()
            return student.name
