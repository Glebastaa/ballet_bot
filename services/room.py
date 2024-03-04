from exceptions import EntityAlreadyExists
from schemas.room import RoomSchema, RoomSchemaAdd, RoomSchemaUpdate
from utils.unitofwork import UnitOfWork


class RoomService:
    def __init__(self) -> None:
        self.uow = UnitOfWork()

    async def _is_already_exists(
            self,
            uow: UnitOfWork,
            studio_id: int,
            room_name: str
    ) -> None:
        filter_by = {
            'studio_id': studio_id,
            'name': room_name
        }
        room = await uow.room.get_all(filter_by)
        if room:
            raise EntityAlreadyExists(
                'Room',
                filter_by
            )

    async def add_room(self, room_name: str, studio_id: int) -> RoomSchema:
        """Add a room to studio."""
        validated_data = RoomSchemaAdd(name=room_name, studio_id=studio_id)
        async with self.uow:
            await self._is_already_exists(self.uow, studio_id, room_name)
            room = await self.uow.room.add(validated_data.model_dump())
            await self.uow.commit()
            return room.to_read_model(RoomSchema)

    async def get_rooms(self, studio_id: int) -> list[RoomSchema]:
        """Gets list of rooms from studio."""
        async with self.uow:
            rooms = await self.uow.room.get_all({'studio_id': studio_id})
            return [room.to_read_model(RoomSchema) for room in rooms]

    async def edit_room(self, room_id: int, new_name: str) -> RoomSchema:
        """Edit a room."""
        validated_data = RoomSchemaUpdate(name=new_name)
        async with self.uow:
            studio_id = (await self.uow.room.get(room_id)).studio_id
            await self._is_already_exists(self.uow, studio_id, new_name)
            room = await self.uow.room.update(
                room_id,
                validated_data.model_dump()
            )
            await self.uow.commit()
            return room.to_read_model(RoomSchema)

    async def delete_room(self, room_id: int) -> str:
        """Delete a room."""
        async with self.uow:
            room = await self.uow.room.delete(room_id)
            await self.uow.commit()
            return room.to_read_model(RoomSchema).name
