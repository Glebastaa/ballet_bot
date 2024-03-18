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
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: Any, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs):
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

    async def get(self, **filters) -> ModelType:
        """Gets a entity by its id."""
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all(self, **filters) -> Sequence[ModelType]:
        """Gets all entities or by filter."""
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def delete(self, **filters) -> ModelType:
        """Delete an existing entity."""
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.scalar(stmt)
        await self.session.delete(res)
        return res

    async def update(self, data: dict[str, Any], **filters) -> ModelType:
        """Update an existing entity."""
        stmt = update(self.model).values(**data).filter_by(
            **filters).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_all(self, filter_by: dict) -> None:
        """Delete all entities by filter."""
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
