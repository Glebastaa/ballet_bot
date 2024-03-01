from pydantic import BaseModel

from schemas.base import NameStr


class StudioSchemaBase(BaseModel):
    name: NameStr


class StudioSchemaAdd(StudioSchemaBase):
    pass


class StudioSchemaUpdate(StudioSchemaBase):
    pass


class StudioSchema(StudioSchemaBase):
    id: int
