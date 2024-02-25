from pydantic import BaseModel


class StudioBase(BaseModel):
    name: str


class StudioAdd(StudioBase):
    pass


class StudioUpdate(StudioBase):
    pass


class StudioRead(StudioBase):
    id: int
