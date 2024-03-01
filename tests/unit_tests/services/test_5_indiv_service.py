# from contextlib import nullcontext as does_not_raise
# from datetime import datetime
# from pydantic import ValidationError

# import pytest

# from sqlalchemy import select
# from sqlalchemy.orm import selectinload

# from database.models import IndividualLesson, WeekDays
# from exceptions import IndivIsFull
# from services.individual_lesson import IndividualLessonService

# from notes import notes_test


# @pytest.mark.indiv_service
# class TestIndividualLesson:
#     async def _get_by_studio_id_or_all(self, session, studio_id: int = None):
#         stmt = select(IndividualLesson)
#         if studio_id:
#             stmt = stmt.where(IndividualLesson.studio_id == studio_id)
#         return await session.scalars(stmt)

#     @pytest.mark.parametrize(
#             'studio_id, start_time, start_date, notes, expectation',
#             [
#                 [1, datetime.strptime('11:11', "%H:%M").time(),
#                  WeekDays.monday, None, does_not_raise()],
#                 [1, datetime.strptime('11:11', "%H:%M").time(),
#                  WeekDays.monday, notes_test, does_not_raise()],
#                 [1, datetime.strptime('11:11', "%H:%M").time(),
#                  WeekDays.monday, -1, pytest.raises(ValidationError)]
#             ]
#     )
#     async def test_add_indiv_lesson(
#         self,
#         session,
#         studios,
#         studio_id,
#         start_time,
#         start_date,
#         notes,
#         expectation
#     ):
#         with expectation:
#             await IndividualLessonService().add_individual_lesson(
#                 studio_id,
#                 start_time,
#                 start_date,
#                 notes
#             )

#             indiv = await self._get_by_studio_id_or_all(session, studio_id)
#             indiv = indiv.all()
#             assert len(indiv) == 1
#             assert indiv[0] is not None
#             assert indiv[0].start_date == start_date
#             assert indiv[0].start_time == start_time

#     async def test_add_dublicate_indiv(self, session, indivs):
#         with does_not_raise():
#             await IndividualLessonService().add_individual_lesson(
#                 1,
#                 datetime.strptime('11:11', "%H:%M").time(),
#                 WeekDays.monday,
#                 None
#             )

#     async def test_get_time_and_date_from_indiv(self, session, indivs):
#         lesson = await IndividualLessonService().get_date_time_from_indiv(1)

#         assert lesson is not None
#         assert lesson[1] == WeekDays.monday
#         assert lesson[0].strftime("%H:%M") == '11:11'

#     async def test_delete_individual_lesson(self, session, indivs):
#         studio_name = await IndividualLessonService(
#             ).delete_individual_lesson(1)

#         indiv = await session.get(IndividualLesson, 1)
#         assert indiv is None
#         assert studio_name == 'Страна огня'

#     async def test_add_student_to_individual_lesson(
#             self,
#             session,
#             indivs,
#             students):
#         await IndividualLessonService().add_student_to_individual_lesson(1, 1)

#         stmt = select(IndividualLesson).where(
#             IndividualLesson.id == 1).options(
#             selectinload(IndividualLesson.students))

#         indiv = await session.scalar(stmt)
#         students = indiv.students
#         assert students[0].name == 'Наруто'
#         await IndividualLessonService().add_student_to_individual_lesson(1, 2)
#         with pytest.raises(IndivIsFull):
#             await IndividualLessonService(
#              ).add_student_to_individual_lesson(1, 3)
