from database.models import Student
from utils.repository import SQLAlchemyRepository


class StudentRepository(SQLAlchemyRepository):
    model = Student
