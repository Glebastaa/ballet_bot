
import pytest

from contextlib import nullcontext as does_not_raise

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Room
from exceptions import EntityAlreadyExists
from schemas.constant import NAME_MAX_LENGTH, NAME_MIN_LENGTH
from services.room import RoomService


@pytest.mark.room_service
class TestRoomService:

    @pytest.mark.parametrize(
            'studio_id, room_name, expectation',
            [
                [1, 'Пещера', does_not_raise()],
                [1, '', pytest.raises(ValidationError)],
                [1, 1, pytest.raises(ValidationError)],
                [1, None, pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MIN_LENGTH - 1),
                 pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MAX_LENGTH + 1),
                 pytest.raises(ValidationError)]
            ]
    )
    async def test_add_room(
        self,
        session,
        studios,
        studio_id,
        room_name,
        expectation
    ):
        with expectation:
            room = await RoomService().add_room(room_name, studio_id)

            room_test = await session.get(Room, 1)
            assert room_test is not None
            assert room_test.name == room_name
            assert room.name == room_name

    async def test_add_duplicate_room(self, session, rooms):
        with pytest.raises(EntityAlreadyExists):
            await RoomService().add_room('Пыточная', 1)

    async def test_get_rooms(
            self,
            session: AsyncSession,
            rooms
    ):
        rooms = await RoomService().get_rooms(1)
        assert rooms is not None
        assert len(rooms) == 3
        for room in rooms:
            assert room.name in ['Столярная', 'Мастерская', 'Пыточная']

    async def test_get_none_rooms(self, session: AsyncSession, studios):
        rooms = await RoomService().get_rooms(1)
        assert rooms == []

    @pytest.mark.parametrize(
            'room_id, new_name, expectation',
            [
                [1, 'Пещера', does_not_raise()],
                [1, '', pytest.raises(ValidationError)],
                [1, 1, pytest.raises(ValidationError)],
                [1, None, pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MIN_LENGTH - 1),
                 pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MAX_LENGTH + 1),
                 pytest.raises(ValidationError)],
                [1, 'Пыточная', pytest.raises(EntityAlreadyExists)]
            ]
    )
    async def test_edit_room(
        self,
        session: AsyncSession,
        rooms,
        room_id,
        new_name,
        expectation
    ):
        with expectation:
            room = await RoomService().edit_room(room_id, new_name)

            assert room is not None
            assert room.name == new_name

            test_room = await session.get(Room, room_id)
            assert test_room is not None
            assert test_room.name == new_name

    async def test_delete_room(self, session, rooms):
        room_name = await RoomService().delete_room(1)
        deleted_room = await session.get(Room, 1)

        assert room_name == 'Столярная'
        assert deleted_room is None
