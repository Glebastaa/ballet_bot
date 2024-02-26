from datetime import time
from database.models import WeekDays
from exceptions import EntityAlreadyExists
from schemas.group import GroupSchema, GroupSchemaAdd, GroupSchemaUpdate
from schemas.schedule import (
    ScheduleSchema,
    ScheduleSchemaAdd,
    ScheduleSchemaUpdate
)

from utils.unitofwork import UnitOfWork


class GroupService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def add_group(
            self,
            group_name: str,
            studio_id: int,
            start_time: time | None = None,
            start_date: WeekDays | None = None
    ) -> GroupSchema:
        "Add a new group."
        validated_group = GroupSchemaAdd(name=group_name, studio_id=studio_id)
        async with self.uow:
            filter_by = {'studio_id': studio_id}
            if await self.uow.group.get_all(filter_by=filter_by):
                raise EntityAlreadyExists

            group = await self.uow.group.add(validated_group.model_dump())

            if start_date and start_time:
                await self.uow.session.flush()
                validated_schedule = ScheduleSchemaAdd(
                    group_id=group.id,
                    start_time=start_time,
                    start_date=start_date
                )
                await self.uow.schedule.add(validated_schedule.model_dump())
            await self.uow.commit()
            return group.to_read_model(GroupSchema)

    async def get_groups(self, studio_id: int) -> list[GroupSchema]:
        "Get list of groups."
        async with self.uow:
            groups = await self.uow.group.get_all(
                {'studio_id': studio_id}
            )
            groups = [group.to_read_model(GroupSchema) for group in groups]
            return groups

    async def edit_group(
            self,
            group_id: int,
            new_group_name: str
    ) -> GroupSchema:
        """Edit group."""
        validated_group = GroupSchemaUpdate(name=new_group_name)
        async with self.uow:
            group = await self.uow.group.update(
                group_id,
                validated_group.model_dump()
            )
            await self.uow.commit()
            return group.to_read_model(GroupSchema)

    async def delete_group(
            self,
            group_id: int
    ) -> str:
        """Delete group."""
        async with self.uow:
            group = await self.uow.group.delete(group_id)
            await self.uow.commit()
            return group.to_read_model(GroupSchema).name

    async def get_date_time_group(
            self,
            group_id: int
    ) -> list[list[str]]:
        """Get datetime."""
        async with self.uow:
            schedules = await self.uow.schedule.get_all(
                {'group_id': group_id}
            )
            schedules = [s.to_read_model(ScheduleSchema) for s in schedules]
            return [[s.start_time.strftime('%H:%M'),
                     s.start_date.value] for s in schedules]

    async def edit_date_time_group(
            self,
            schedule_id: int,
            new_date: WeekDays | None = None,
            new_time: time | None = None
    ) -> ScheduleSchema:
        """Edit date."""
        validated_data = ScheduleSchemaUpdate(
            start_date=new_date,
            start_time=new_time
        )
        async with self.uow:
            schedule = await self.uow.schedule.update(
                schedule_id,
                validated_data.model_dump(exclude_none=True)
            )
            await self.uow.commit()
            return schedule.to_read_model(ScheduleSchema)
