from typing import Type
from schemas.studio import StudioSchema, StudioSchemaAdd, StudioSchemaUpdate
from utils.unitofwork import UnitOfWork


class StudioService:
    def __init__(self):
        self.uow: Type[UnitOfWork] = UnitOfWork()

    async def add_studio(self, studio_name: str) -> StudioSchema:
        studio_dict = StudioSchemaAdd(name=studio_name).model_dump()
        async with self.uow:
            st = await self.uow.studio.add(studio_dict)
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
        new_studio = StudioSchemaUpdate(name=new_name)
        async with self.uow:
            studio = await self.uow.studio.update(
                studio_id,
                new_studio.model_dump()
            )
            await self.uow.commit()
            return studio.to_read_model(StudioSchema)

    async def delete_studio(self, studio_id: int) -> str:
        async with self.uow:
            studio = await self.uow.studio.delete(studio_id)
            await self.uow.commit()
            return studio.name
