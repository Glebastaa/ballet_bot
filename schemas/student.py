from pydantic import BaseModel

from schemas.base import NameStr


class StudentSchemaBase(BaseModel):
    name: NameStr
    notes: str | None = None


class StudentSchemaAdd(StudentSchemaBase):
    pass


class StudentSchema(StudentSchemaBase):
    id: int

    class Config:
        from_attributes = True


class StudentSchemaUpdate(StudentSchemaBase):
    pass


class StudentNotesSchema(BaseModel):
    notes: str | None
