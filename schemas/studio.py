from pydantic import BaseModel


class StudioSchemaBase(BaseModel):
    name: str


class StudioSchemaAdd(StudioSchemaBase):
    pass


class StudioSchemaUpdate(StudioSchemaBase):
    pass


class StudioSchema(StudioSchemaBase):
    id: int
