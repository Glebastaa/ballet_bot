from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, Type, TypeVar
from pydantic import BaseModel

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import Base


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, data: Any):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, pk_or_obj: int | Any):
        raise NotImplementedError

    @abstractmethod
    async def update(self, pk: int, data: Any):
        raise NotImplementedError

    @abstractmethod
    async def get(self, pk: int):
        raise NotImplementedError


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class SQLAlchemyRepository(AbstractRepository, Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session: AsyncSession = session

    async def add(self, data: dict[str, Any]) -> ModelType:
        """Create a new entity."""
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, id: int) -> ModelType:
        """Gets a entity by its id."""
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self, **filter_by) -> Sequence[ModelType]:
        """Gets all entities or by filter."""
        stmt = select(self.model)
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def delete(self, id: int) -> ModelType:
        """Delete an existing entity."""
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.scalar(stmt)
        await self.session.delete(res)
        return res

    async def update(self, id: int, data: dict[str, Any]) -> ModelType:
        """Update an existing entity."""
        stmt = update(self.model).values(**data).filter_by(
            id=id).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_all(self, filter_by: dict) -> None:
        """Delete all entities by filter."""
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
