import pytest
from sqlalchemy import select

from database.db_api.studio import add_studio, edit_studio, get_studios
from database.models import Studio
from exceptions import EntityAlreadyExists

class TestStudio:
    async def test_add_studio(self, session, studio_names):
        await add_studio(session, studio_names['studio_one'])

        stmt = select(Studio).where(Studio.name == studio_names['studio_one'])
        studio = await session.execute(stmt)

        assert studio.scalar_one_or_none().name == studio_names['studio_one']

    async def test_add_dublicate_studio(self, session, studio_names):
        with pytest.raises(EntityAlreadyExists):
            await add_studio(session, studio_names['studio_one'])

        stmt = select(Studio)
        studios = await session.execute(stmt)
        assert len(studios.scalars().all()) == 1

    async def test_add_second_studio(self, session, studio_names):
        await add_studio(session, studio_names['studio_two'])

        stmt = select(Studio)
        studios = await session.execute(stmt)
        assert len(studios.scalars().all()) == 2

    async def test_get_studios(self, session):
        studios = await get_studios(session)

        assert len(studios) == 2
        assert studios[0].name == 'strana ognya'
        assert studios[1].name == 'strana wodi'

    async def test_edit_studios(self, session):
        data = {
            'id': 1,
            'new_name': 'strana_zemli'
        }

        await edit_studio(session, data['id'], data['new_name'])

        stmt = select(Studio).where(Studio.name == 'strana_zemli')
        studio = await session.execute(stmt)
        studio = studio.scalar_one_or_none()
        assert studio.name == data['new_name']
        assert studio.id == data['id']

