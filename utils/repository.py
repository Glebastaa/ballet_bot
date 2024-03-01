from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    @abstractmethod
    async def add():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError

    @abstractmethod
    async def update():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, id: int):
        """Get a entity by id or None."""
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, filter_by: dict = None):
        stmt = select(self.model)
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def delete(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.scalar(stmt)
        await self.session.delete(res)
        return res

    async def update(self, id: int, data: dict):
        stmt = update(self.model).values(**data).where(
            self.model.id == id).returning(self.model)
        res = await self.session.scalar(stmt)
        return res
