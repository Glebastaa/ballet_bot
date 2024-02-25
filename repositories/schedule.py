from database.models import Schedule
from utils.repository import SQLAlchemyRepository


class ScheduleRepository(SQLAlchemyRepository):
    model = Schedule
