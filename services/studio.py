from typing import Type

from exceptions import EntityAlreadyExists
from schemas.studio import StudioSchema, StudioSchemaAdd, StudioSchemaUpdate
from utils.unitofwork import UnitOfWork


class StudioService:
    def __init__(self):
        self.uow: Type[UnitOfWork] = UnitOfWork()

    async def _is_already_exists(self, name: str, uow: UnitOfWork) -> None:
        if await self.uow.studio.get_all({'name': name}):
            raise EntityAlreadyExists(
                'Studio',
                {'name': name}
            )

    async def add_studio(self, studio_name: str) -> StudioSchema:
        validated_data = StudioSchemaAdd(name=studio_name)
        async with self.uow:
            await self._is_already_exists(studio_name, self.uow)
            st = await self.uow.studio.add(validated_data.model_dump())
            await self.uow.commit()
            return st.to_read_model(StudioSchema)

    async def get_studios(self) -> list[StudioSchema]:
        async with self.uow:
            studios = await self.uow.studio.get_all()
            return [st.to_read_model(StudioSchema) for st in studios]

    async def edit_studio(
            self,
            studio_id: int,
            new_name: str
            ) -> StudioSchema:
        """Edit studio' name."""
        validated_data = StudioSchemaUpdate(name=new_name)
        async with self.uow:
            await self._is_already_exists(new_name, self.uow)
            studio = await self.uow.studio.update(
                studio_id,
                validated_data.model_dump()
            )
            await self.uow.commit()
            return studio.to_read_model(StudioSchema)

    async def delete_studio(self, studio_id: int) -> str:
        async with self.uow:
            studio = await self.uow.studio.delete(studio_id)
            await self.uow.commit()
            return studio.name
