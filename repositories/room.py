from database.models import Room
from utils.repository import SQLAlchemyRepository


class RoomRepository(SQLAlchemyRepository):
    model = Room