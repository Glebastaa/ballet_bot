from database.models import Studio
from utils.repository import SQLAlchemyRepository


class StudioRepository(SQLAlchemyRepository):
    model = Studio
