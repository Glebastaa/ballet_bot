from datetime import time
from pydantic import BaseModel

from database.models import WeekDays


class ScheduleSchemaBase(BaseModel):
    start_time: time
    start_date: WeekDays


class ScheduleSchemaAdd(ScheduleSchemaBase):
    group_id: int


class ScheduleSchema(ScheduleSchemaBase):
    group_id: int

    class Config:
        from_attributes = True


class ScheduleSchemaUpdate(ScheduleSchemaBase):
    start_time: time | None = None
    start_date: WeekDays | None = None
