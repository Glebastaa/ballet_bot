from pydantic import BaseModel, PositiveInt

from schemas.base import NameStr


class GroupSchemaBase(BaseModel):
    name: NameStr | None
    notes: str | None = None
    is_individual: bool


class GroupSchemaAdd(GroupSchemaBase):
    name: NameStr
    studio_id: PositiveInt


class GroupSchema(GroupSchemaBase):
    id: int
    name: NameStr
    notes: str | None
    studio_id: int

    class Config:
        from_attributes = True


class GroupSchemaUpdate(GroupSchemaBase):
    pass
