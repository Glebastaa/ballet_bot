from database.models import Studio
from utils.repository import SQLAlchemyRepository


class StudioRepository(SQLAlchemyRepository[Studio]):
    pass
