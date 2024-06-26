from database.models import User
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    pass
