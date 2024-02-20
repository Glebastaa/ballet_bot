import pytest
from sqlalchemy import select

from database.db_api.studio import (
    add_studio, delete_studio, edit_studio, get_studios)
from database.models import Studio
from exceptions import EntityAlreadyExists


class TestStudio:
    async def _get_by_name(self, session, name: str = None):
        stmt = select(Studio)
        if name:
            stmt = stmt.where(Studio.name == name)
        return await session.execute(stmt)

    async def test_add_studio(self, session, first_studio):
        await add_studio(session, first_studio)

        studio = await self._get_by_name(session, first_studio)
        assert studio.scalar_one_or_none().name == first_studio

    async def test_add_dublicate_studio(self, session, first_studio):
        with pytest.raises(EntityAlreadyExists):
            await add_studio(session, first_studio)

        studios = await self._get_by_name(session, first_studio)
        assert len(studios.scalars().all()) == 1

    async def test_add_second_third_studios(self, session, second_studio):
        await add_studio(session, second_studio)
        await add_studio(session, 'Страна ветра')

        studios = (await self._get_by_name(session)).scalars().all()
        assert len(studios) == 3
        assert studios[1].name == second_studio

    async def test_get_studios(self, session, first_studio, second_studio):
        studios = await get_studios(session)

        assert len(studios) == 3
        assert studios[0].name == first_studio
        assert studios[1].name == second_studio

    async def test_edit_studios(self, session, new_studio_data):
        await edit_studio(session, *new_studio_data.values())

        studio = await self._get_by_name(session, new_studio_data['new_name'])
        studio = studio.scalar_one_or_none()

        assert studio.name == new_studio_data['new_name']
        assert studio.id == new_studio_data['id']

    async def test_delete_studio(self, session, new_studio_data):
        await delete_studio(session, new_studio_data['id'])

        studio = await self._get_by_name(session, new_studio_data['new_name'])
        studio = studio.scalar_one_or_none()

        assert studio is None
