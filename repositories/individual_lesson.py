from database.models import IndividualLesson
from utils.repository import SQLAlchemyRepository


class IndividualLessonRepository(SQLAlchemyRepository):
    model = IndividualLesson
