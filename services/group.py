from datetime import datetime, time, timedelta
from database.models import WeekDays
from exceptions import EntityAlreadyExists, ScheduleTimeInsertionError
from schemas.group import GroupSchema, GroupSchemaAdd, GroupSchemaUpdate
from schemas.schedule import (
    ScheduleSchema,
    ScheduleSchemaAdd,
    ScheduleSchemaUpdate
)

from utils.unitofwork import UnitOfWork

LESSON_DURATION = 1


class GroupService:
    def __init__(self) -> None:
        self.uow = UnitOfWork()

    async def _is_already_exists(
            self,
            studio_id: int,
            uow: UnitOfWork,
            is_individual: bool,
            group_name: str | None = None
    ) -> None:
        filter_by = {
            'studio_id': studio_id,
            'name': group_name,
            'is_individual': is_individual
        }
        if await uow.group.get_all(filter_by=filter_by):
            raise EntityAlreadyExists(
                'Group',
                filter_by
            )

    async def _time_not_busy(
            self,
            room_id: int,
            start_time: time,
            start_date: WeekDays,
            uow: UnitOfWork,
            schedule_id: int | None = None
    ) -> None:
        schedules = await uow.schedule.get_all(
            {
                'room_id': room_id,
                'start_date': start_date
            }
        )
        new_time = datetime.combine(datetime.today(), start_time)
        td = timedelta(hours=LESSON_DURATION)
        for schedule in schedules:
            # Check for update time.
            if schedule.id == schedule_id:
                continue

            timeslot = datetime.combine(datetime.today(), schedule.start_time)
            if new_time == timeslot:
                raise ScheduleTimeInsertionError
            if abs(new_time - timeslot) == td:
                break
            # Add lesson duration.
            if abs(new_time - (timeslot + td)) < td:
                raise ScheduleTimeInsertionError
            if abs(new_time - (timeslot - td)) < td:
                raise ScheduleTimeInsertionError

    async def add_group(
            self,
            group_name: str,
            studio_id: int,
            notes: str = None,
            is_individual: bool = False
    ) -> GroupSchema:
        "Add a new group or a individual lesson."
        validated_data = GroupSchemaAdd(
            name=group_name,
            studio_id=studio_id,
            is_individual=is_individual,
            notes=notes
        )
        async with self.uow:
            await self._is_already_exists(
                group_name=group_name,
                studio_id=studio_id,
                is_individual=is_individual,
                uow=self.uow
            )
            group = await self.uow.group.add(validated_data.model_dump())
            await self.uow.commit()
            return group.to_read_model(GroupSchema)

    async def add_schedule_to_group(
            self,
            group_id: int,
            room_id: int,
            start_time: time,
            start_date: WeekDays
    ) -> ScheduleSchema:
        "Add schedule to group."
        validated_data = ScheduleSchemaAdd(
            group_id=group_id,
            room_id=room_id,
            start_time=start_time,
            start_date=start_date
        )
        async with self.uow:
            # Check that the time is not busy.
            await self._time_not_busy(
                room_id=room_id,
                start_time=start_time,
                start_date=start_date,
                uow=self.uow
            )
            schedule = await self.uow.schedule.add(validated_data.model_dump())
            await self.uow.commit()
            return schedule

    async def get_groups(
            self,
            studio_id: int,
            is_individual: bool = False
    ) -> list[GroupSchema]:
        "Get list of groups or list of individual lessons."
        async with self.uow:
            groups = await self.uow.group.get_all(
                {
                    'studio_id': studio_id,
                    'is_individual': is_individual
                }
            )
            return [group.to_read_model(GroupSchema) for group in groups]

    async def edit_group(
            self,
            group_id: int,
            new_group_name: str,
            is_individual: bool = False
    ) -> GroupSchema:
        """Edit group."""
        validated_group = GroupSchemaUpdate(
            name=new_group_name,
            is_individual=is_individual
        )
        async with self.uow:
            old_group = await self.uow.group.get(group_id)
            await self._is_already_exists(
                group_name=new_group_name,
                studio_id=old_group.studio_id,
                is_individual=is_individual,
                uow=self.uow
            )
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
        """Delete group or inividual lesson."""
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
            return [[(await self.uow.room.get(s.room_id)).name,
                     s.start_time.strftime('%H:%M'),
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
            old_schedule = await self.uow.schedule.get(schedule_id)
            if not new_date:
                new_date = old_schedule.start_date
            elif not new_time:
                new_time = old_schedule.start_time
            await self._time_not_busy(
                room_id=old_schedule.room_id,
                start_time=new_time,
                start_date=new_date,
                uow=self.uow,
                schedule_id=schedule_id
            )

            schedule = await self.uow.schedule.update(
                schedule_id,
                validated_data.model_dump(exclude_none=True)
            )
            await self.uow.commit()
            return schedule.to_read_model(ScheduleSchema)

    async def get_groups_from_student(
        self,
        student_id: int,
        is_individual: bool = False
    ) -> list[GroupSchema]:
        async with self.uow:
            student = await self.uow.student.get(student_id)
            await self.uow.session.refresh(student, attribute_names=['groups'])
            groups = [
                group.to_read_model(GroupSchema) for group in student.groups
                if group.is_individual == is_individual
            ]
            return groups
