import pytest

from contextlib import nullcontext as does_not_raise

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.models import Group, Student
from exceptions import IndivIsFull, InvalidIsIndividual, StudentAlreadyInGroupError
from schemas.constant import NAME_MAX_LENGTH, NAME_MIN_LENGTH
from services.student import StudentService


@pytest.mark.student_service
class TestStudentService:
    @pytest.mark.parametrize(
            'student_name, expectation',
            [
                ['Конохамару', does_not_raise()],
                ['', pytest.raises(ValidationError)],
                [1, pytest.raises(ValidationError)],
                [None, pytest.raises(ValidationError)],
                ['А' * (NAME_MIN_LENGTH - 1), pytest.raises(ValidationError)],
                ['А' * (NAME_MAX_LENGTH + 1), pytest.raises(ValidationError)]
            ]
    )
    async def test_add_student(self, session, student_name, expectation):
        with expectation:
            await StudentService().add_student(student_name)

            student = await session.execute(select(Student))
            student = student.scalars().all()
            assert len(student) == 1
            assert student[0].name == student_name

    async def test_add_dublicate_student(self, session, students):
        await StudentService().add_student('Наруто')
        student_1 = await session.get(Student, 1)
        student_2 = await session.get(Student, 4)

        assert student_1.name == student_2.name

    @pytest.mark.parametrize(
            'st_id, gr_id, is_individual, expectation, st_name, gr_name',
            [
                [1, 1, False, does_not_raise(), 'Наруто', 'Коноха'],
                [1, 1, True, pytest.raises(InvalidIsIndividual), 'Наруто',
                 'Коноха'],
                [1, 4, True, does_not_raise(), 'Наруто', 'indiv№1'],
            ]
    )
    async def test_add_student_to_group(
        self,
        session,
        indivs,
        students,
        st_id,
        gr_id,
        is_individual,
        expectation,
        st_name,
        gr_name
    ):
        with expectation:
            await StudentService().add_student_to_group(
                st_id,
                gr_id,
                is_individual
            )

            stmt = select(Group).where(Group.id == gr_id).options(
                selectinload(Group.students))

            group = await session.scalar(stmt)
            students = group.students
            assert students[0].name == st_name
            assert group.name == gr_name

    @pytest.mark.parametrize(
            'group_id, is_individual, expectation',
            [
                [2, False, does_not_raise()],
                [5, True, pytest.raises(IndivIsFull)]
            ]
    )
    async def test_add_multiple_students_to_group_or_indiv(
            self,
            session,
            students,
            indivs,
            group_id,
            is_individual,
            expectation
    ):
        with expectation:
            await StudentService().add_student_to_group(
                1, group_id, is_individual)
            await StudentService().add_student_to_group(
                2, group_id, is_individual)
            await StudentService().add_student_to_group(
                3, group_id, is_individual)

            stmt = select(Group).where(Group.id == group_id).options(
                        selectinload(Group.students))

            group = await session.scalar(stmt)
            assert len(group.students) == 3
            for student in group.students:
                assert student.name in ['Саске', 'Сакура', 'Наруто']

    async def test_add_already_in_group_student(self, session, students_groups):
        with pytest.raises(StudentAlreadyInGroupError):
            await StudentService().add_student_to_group(1, 1)

    @pytest.mark.parametrize(
            'id, fake_id, ln, st_list, expectation',
            [
                [1, 2, 3, ['Саске', 'Сакура', 'Наруто'], does_not_raise()],
                [4, 5, 2, ['Саске', 'Наруто'], does_not_raise()]
            ]
    )
    async def test_get_students_from_group(
            self,
            session,
            students_indivs,
            id,
            fake_id,
            ln,
            st_list,
            expectation
    ):
        with expectation:
            students = await StudentService().get_students_from_group(id)
            students_2 = await StudentService(
            ).get_students_from_group(fake_id)

            assert students is not None
            assert len(students) == ln
            for student in students:
                assert student.name in st_list

            assert [] == students_2

    async def test_delete_student_from_group(self, session, students_groups):
        name = await StudentService().delete_student_from_group(1, 1)

        stmt = select(Group).where(Group.id == 1).options(
            selectinload(Group.students))
        group = await session.scalar(stmt)
        assert set(
            [student.name for student in group.students]
        ) == set(['Саске', 'Сакура'])
        assert name == 'Наруто'

    @pytest.mark.parametrize(
            'student_id, new_name, expectation',
            [
                [1, 'Уи-чан', does_not_raise()],
                [1, '', pytest.raises(ValidationError)],
                [1, 1, pytest.raises(ValidationError)],
                [1, None, pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MIN_LENGTH - 1),
                 pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MAX_LENGTH + 1),
                 pytest.raises(ValidationError)]
            ]
    )
    async def test_edit_student_name(
        self,
        session,
        students,
        student_id,
        new_name,
        expectation
    ):
        with expectation:
            old_name = (await session.get(Student, student_id)).name
            await StudentService().edit_student(student_id, new_name)

            new_student = await session.get(Student, student_id)
            assert new_student.name == new_name
            assert old_name != new_student.name

    async def test_delete_student(self, session, students_groups):
        name = await StudentService().delete_student(1)

        student = await session.get(Student, 1)
        assert student is None
        assert name == 'Наруто'

        stmt = select(Group).where(Group.id == 1).options(
            selectinload(Group.students)
        )
        group = await session.scalar(stmt)
        for st in group.students:
            assert st.id != 1

    async def test_get_all_students(self, session, students):
        students = await StudentService().get_all_students()

        assert set(
            [student.name for student in students]
        ) == set(['Саске', 'Сакура', 'Наруто'])

    async def test_get_none_students(self, session):
        none_students = await StudentService().get_all_students()

        assert none_students == []
