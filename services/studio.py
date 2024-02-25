from typing import Type
from schemas.studio import StudioAdd, StudioUpdate
from database.models import Studio
from utils.unitofwork import UnitOfWork


class StudioService:
    def __init__(self):
        self.uow: Type[UnitOfWork] = UnitOfWork()

    async def add_studio(self, studio_name: str) -> Studio:
        studio_dict = StudioAdd(name=studio_name).model_dump()
        async with self.uow:
            st = await self.uow.studio.add(studio_dict)
            await self.uow.commit()
            return st

    async def get_studios(self) -> list[Studio]:
        async with self.uow:
            return await self.uow.studio.get_all()

    async def edit_studio(
            self,
            studio_id: int,
            new_name: str
            ) -> Studio:
        """Edit studio' name."""
        new_studio = StudioUpdate(name=new_name)
        async with self.uow:
            studio = await self.uow.studio.update(
                studio_id,
                new_studio.model_dump()
            )
            await self.uow.commit()
            return studio

    async def delete_studio(self, studio_id: int) -> str:
        async with self.uow:
            studio = await self.uow.studio.delete(studio_id)
            await self.uow.commit()
            return studio.name
