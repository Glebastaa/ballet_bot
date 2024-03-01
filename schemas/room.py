from pydantic import BaseModel

from schemas.base import NameStr


class RoomSchemaBase(BaseModel):
    name: NameStr


class RoomSchemaAdd(RoomSchemaBase):
    studio_id: int


class RoomSchema(RoomSchemaBase):
    id: int
    studio_id: int


class RoomSchemaUpdate(RoomSchemaBase):
    pass
