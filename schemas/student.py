from pydantic import BaseModel


class StudentSchemaBase(BaseModel):
    name: str
    notes: str | None = None


class StudentSchemaAdd(StudentSchemaBase):
    pass


class StudentSchema(StudentSchemaBase):
    id: int
    individual_lesson_id: int | None

    class Config:
        from_attributes = True


class StudentSchemaUpdate(StudentSchemaBase):
    pass
