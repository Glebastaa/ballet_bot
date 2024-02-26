from datetime import time
from pydantic import BaseModel

from database.models import WeekDays


class IndivSchemaBase(BaseModel):
    start_time: time
    start_date: WeekDays
    notes: str | None


class IndivSchemaAdd(IndivSchemaBase):
    studio_id: int


class IndivSchemaUpdate(IndivSchemaBase):
    pass


class IndivSchema(IndivSchemaBase):
    id: int
    studio_id: int
