from database.models import Group
from utils.repository import SQLAlchemyRepository


class GroupRepository(SQLAlchemyRepository[Group]):
    pass
