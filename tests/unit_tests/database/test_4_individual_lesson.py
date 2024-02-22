import pytest

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.db_api.individual_lesson import (
    add_individual_lesson,
    add_student_to_individual_lesson,
    delete_individual_lesson,
    get_date_time_individual_lesson
)
from database.models import IndividualLesson, WeekDays


@pytest.mark.indiv
class TestIndividualLesson:
    async def _get_by_studio_id_or_all(self, session, studio_id: int = None):
        stmt = select(IndividualLesson)
        if studio_id:
            stmt = stmt.where(IndividualLesson.studio_id == studio_id)
        return await session.scalars(stmt)

    async def test_add_indiv_lesson(self, session, studios):
        await add_individual_lesson(
            session,
            1,
            datetime.strptime('11:11', "%H:%M").time(),
            WeekDays.monday
        )

        indiv = await self._get_by_studio_id_or_all(session)
        indiv = indiv.all()
        assert len(indiv) == 1
        assert indiv[0] is not None
        assert indiv[0].start_date == WeekDays.monday
        assert indiv[0].start_time.strftime("%H:%M") == '11:11'

    async def test_get_time_and_date_from_indiv(self, session, indivs):
        data = await get_date_time_individual_lesson(session, 1)

        assert data is not None
        assert data[1] == WeekDays.monday
        assert data[0].strftime("%H:%M") == '11:11'

    async def test_delete_individual_lesson(self, session, indivs):
        await delete_individual_lesson(session, 1)

        indiv = await session.get(IndividualLesson, 1)
        assert indiv is None

    async def test_add_student_to_individual_lesson(
            self,
            session,
            indivs,
            students):
        await add_student_to_individual_lesson(session, 1, 1)

        stmt = select(IndividualLesson).where(
            IndividualLesson.id == 1).options(
                selectinload(IndividualLesson.students))
        indiv = await session.scalar(stmt)
        assert 1 == indiv.students[0].id
