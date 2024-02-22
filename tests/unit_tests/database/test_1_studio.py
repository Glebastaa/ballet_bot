import pytest
from sqlalchemy import select

from database.db_api.studio import (
    add_studio, delete_studio, edit_studio, get_studios)
from database.models import Studio
from exceptions import EntityAlreadyExists


@pytest.mark.studio
class TestStudio:
    async def _get_by_name_or_all(self, session, name: str = None):
        stmt = select(Studio)
        if name:
            stmt = stmt.where(Studio.name == name)
        return await session.execute(stmt)

    async def test_add_studio(self, session):
        await add_studio(session, 'Страна огня')

        studio = await self._get_by_name_or_all(session, 'Страна огня')
        assert studio.scalar_one_or_none().name == 'Страна огня'

    async def test_add_dublicate_studio(self, session, studios):
        with pytest.raises(EntityAlreadyExists):
            await add_studio(session, 'Страна огня')

        studios = await self._get_by_name_or_all(session)
        assert len(studios.scalars().all()) == 3

    async def test_get_studios(self, session, studios):
        studios = await get_studios(session)

        name_list = ['Страна огня', 'Страна воды', 'Страна ветра']
        studio_names = [studio.name for studio in studios]

        assert len(studios) == 3
        assert set(name_list) == set(studio_names)

    async def test_edit_studios(self, session, studios):
        await edit_studio(session, 1, 'Яметте кудасай, ониии-чан!')
        studio = await session.get(Studio, 1)
        assert studio.name == 'Яметте кудасай, ониии-чан!'

    async def test_delete_studio(self, session, studios):
        await delete_studio(session, 1)

        studio = await session.get(Studio, 1)
        assert studio is None
