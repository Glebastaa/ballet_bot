from database.models import Room
from utils.repository import SQLAlchemyRepository


class RoomRepository(SQLAlchemyRepository[Room]):
    pass
