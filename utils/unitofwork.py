from abc import ABC, abstractmethod

from database.db import async_session_maker, engine
from database.models import Group, Room, Schedule, Student, Studio, User
from repositories.group import GroupRepository
from repositories.room import RoomRepository
from repositories.schedule import ScheduleRepository
from repositories.student import StudentRepository
from repositories.studio import StudioRepository
from repositories.user import UserRepository


class IUnitOfWork(ABC):
    studio: StudioRepository
    group: GroupRepository
    schedule: ScheduleRepository
    student: StudentRepository
    room: RoomRepository
    user: UserRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker
        self.engine = engine

    async def __aenter__(self):
        self.session = self.session_factory()

        self.studio = StudioRepository(Studio, self.session)
        self.group = GroupRepository(Group, self.session)
        self.schedule = ScheduleRepository(Schedule, self.session)
        self.student = StudentRepository(Student, self.session)
        self.room = RoomRepository(Room, self.session)
        self.user = UserRepository(User, self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.engine.dispose()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
