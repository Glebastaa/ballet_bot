from datetime import datetime, time, timedelta

from database.models import WeekDays
from exceptions import EntityAlreadyExists, ScheduleTimeInsertionError
from logger_config import setup_logger
from schemas.group import GroupSchema, GroupSchemaAdd, GroupSchemaUpdate
from schemas.schedule import (
    ScheduleSchema,
    ScheduleSchemaAdd,
    ScheduleSchemaUpdate
)
from utils.unitofwork import UnitOfWork

LESSON_DURATION = 1

logger = setup_logger('group')


class GroupService:
    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    async def _is_already_exists(
            self,
            studio_id: int,
            uow: UnitOfWork,
            is_individual: bool,
            group_name: str | None = None
    ) -> None:
        filters = {
            'studio_id': studio_id,
            'name': group_name,
            'is_individual': is_individual
        }
        if await uow.group.get_all(**filters):
            logger.error(
                f'Группа "{group_name}" в студии по id {studio_id} '
                'уже существует.'
            )
            raise EntityAlreadyExists(
                'Group',
                filters
            )

    async def _time_not_busy(
            self,
            group_id: int,
            start_time: time,
            start_date: WeekDays,
            uow: UnitOfWork,
            schedule_id: int | None = None
    ) -> None:
        schedules = await uow.schedule.get_all(
            group_id=group_id,
            start_date=start_date
        )
        new_time = datetime.combine(datetime.today(), start_time)
        td = timedelta(hours=LESSON_DURATION)
        for schedule in schedules:
            # Check for update time.
            if schedule.id == schedule_id:
                continue

            timeslot = datetime.combine(datetime.today(), schedule.start_time)
            log_msg = (
                    f'Невозможно добавить расписание. Время '
                    f'{start_time} уже занято или слишком близко к '
                    'существующему расписанию.'
                )
            if new_time == timeslot:
                logger.error(log_msg)
                raise ScheduleTimeInsertionError
            if abs(new_time - timeslot) == td:
                break
            # Add lesson duration.
            if abs(new_time - (timeslot + td)) < td:
                logger.error(log_msg)
                raise ScheduleTimeInsertionError
            if abs(new_time - (timeslot - td)) < td:
                logger.error(log_msg)
                raise ScheduleTimeInsertionError

    async def add_group(
            self,
            group_name: str,
            studio_id: int,
            notes: str | None = None,
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
            logger.info(
                f'Группа "{group_name}" добавлена в студию {studio_id}'
            )
            return group.to_read_model(GroupSchema)

    async def add_schedule_to_group(
            self,
            group_id: int,
            start_time: time,
            start_date: WeekDays
    ) -> ScheduleSchema:
        "Add a schedule to group."
        validated_data = ScheduleSchemaAdd(
            group_id=group_id,
            start_time=start_time,
            start_date=start_date
        )
        async with self.uow:
            # Check that the time is not busy.
            await self._time_not_busy(
                group_id=group_id,
                start_time=start_time,
                start_date=start_date,
                uow=self.uow
            )
            schedule = await self.uow.schedule.add(validated_data.model_dump())
            await self.uow.commit()
            logger.info(
                f'Рассписание "{start_time}" - "{start_date.value}" добавлено '
                f'для группы {group_id}'
            )
            return schedule.to_read_model(ScheduleSchema)

    async def get_groups(
            self,
            studio_id: int,
            is_individual: bool = False
    ) -> list[GroupSchema]:
        "Gets list of groups or list of individual lessons."
        async with self.uow:
            groups = await self.uow.group.get_all(
                studio_id=studio_id,
                is_individual=is_individual
            )
            return [group.to_read_model(GroupSchema) for group in groups]

    async def edit_group(
            self,
            group_id: int,
            new_group_name: str | None = None,
            notes: str | None = None,
            is_individual: bool = False
    ) -> GroupSchema:
        """Edit a group."""
        validated_group = GroupSchemaUpdate(
            name=new_group_name,
            notes=notes,
            is_individual=is_individual
        )
        async with self.uow:
            if new_group_name:
                old_group = await self.uow.group.get(id=group_id)
                await self._is_already_exists(
                    group_name=new_group_name,
                    studio_id=old_group.studio_id,
                    is_individual=is_individual,
                    uow=self.uow
                )
            group = await self.uow.group.update(
                data=validated_group.model_dump(exclude_none=True),
                id=group_id
            )
            await self.uow.commit()
            logger.info(
                f'У группы по id {group_id} изменены данные '
                f'на "{validated_group.model_dump(exclude_none=True)}".'
            )
            return group.to_read_model(GroupSchema)

    async def delete_group(
            self,
            group_id: int
    ) -> str:
        """Delete a group or inividual lesson."""
        async with self.uow:
            group = await self.uow.group.delete(id=group_id)
            await self.uow.commit()
            logger.info(f'Группа "{group.name}" удалена.')
            return group.to_read_model(GroupSchema).name

    async def get_date_time_group(
            self,
            group_id: int
    ) -> list[ScheduleSchema]:
        """Gets a datetime."""
        async with self.uow:
            schedules = await self.uow.schedule.get_all(group_id=group_id)
            return [s.to_read_model(ScheduleSchema) for s in schedules]

    async def get_date_time_indivs_by_studio(
            self,
            studio_id: int
    ) -> list[ScheduleSchema]:
        """Gets all datetime from studio."""
        async with self.uow:
            studio = await self.uow.studio.get(id=studio_id)
            res: list = []
            for group in studio.groups:
                if group.is_individual:
                    schedules = await self.uow.schedule.get_all(
                        group_id=group.id
                    )
                    res.extend(schedules)
            return [r.to_read_model(ScheduleSchema) for r in res]

    async def edit_date_time_group(
            self,
            schedule_id: int,
            new_date: WeekDays | None = None,
            new_time: time | None = None
    ) -> ScheduleSchema:
        """Edit a date."""
        validated_data = ScheduleSchemaUpdate(
            start_date=new_date,
            start_time=new_time
        )
        async with self.uow:
            old_schedule = await self.uow.schedule.get(id=schedule_id)
            if not new_date:
                new_date = old_schedule.start_date
            if not new_time:
                new_time = old_schedule.start_time
            await self._time_not_busy(
                group_id=old_schedule.group_id,
                start_time=new_time,
                start_date=new_date,
                uow=self.uow,
                schedule_id=schedule_id
            )

            schedule = await self.uow.schedule.update(
                data=validated_data.model_dump(exclude_none=True),
                id=schedule_id
            )
            await self.uow.commit()
            logger.info(
                f'Расписание: "{old_schedule.start_date.value}" - '
                f'{old_schedule.start_time} изменено на '
                f'"{schedule.start_date.value}" - {schedule.start_time}.'
            )
            return schedule.to_read_model(ScheduleSchema)

    async def get_groups_from_student(
        self,
        student_id: int,
        is_individual: bool = False
    ) -> list[GroupSchema]:
        """Gets a list of groups by student id."""
        async with self.uow:
            student = await self.uow.student.get(id=student_id)
            await self.uow.session.refresh(student, attribute_names=['groups'])
            groups = [
                group.to_read_model(GroupSchema) for group in student.groups
                if group.is_individual == is_individual
            ]
            return groups

    async def delete_notes(self, group_id: int) -> None:
        """Set notes to None."""
        async with self.uow:
            await self.uow.group.update({'notes': None}, id=group_id)
            await self.uow.commit()

    async def get_notes(self, group_id: int) -> str | None:
        """Get notes by group id."""
        async with self.uow:
            group = await self.uow.group.get(id=group_id)
            return group.notes
