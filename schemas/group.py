from pydantic import BaseModel


class GroupSchemaBase(BaseModel):
    name: str
    notes: str | None = None


class GroupSchemaAdd(GroupSchemaBase):
    studio_id: int


class GroupSchema(GroupSchemaBase):
    id: int
    notes: str | None
    studio_id: int

    class Config:
        from_attributes = True


class GroupSchemaUpdate(GroupSchemaBase):
    pass
