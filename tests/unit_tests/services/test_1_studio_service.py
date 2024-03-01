import pytest

from contextlib import nullcontext as does_not_raise

from pydantic import ValidationError
from sqlalchemy import select

from database.models import Studio
from exceptions import EntityAlreadyExists
from schemas.constant import NAME_MAX_LENGTH, NAME_MIN_LENGTH
from services.studio import StudioService


@pytest.mark.studio_service
class TestStudioService:
    @pytest.mark.parametrize(
            'name, expectation',
            [
                ['Акихабара', does_not_raise()],
                ['', pytest.raises(ValidationError)],
                [1, pytest.raises(ValidationError)],
                ['А' * (NAME_MIN_LENGTH - 1), pytest.raises(ValidationError)],
                ['А' * (NAME_MAX_LENGTH + 1), pytest.raises(ValidationError)],
            ]
    )
    async def test_add_studio(self, session, name, expectation):
        with expectation:
            await StudioService().add_studio(name)
            studio = await session.execute(select(Studio))
            studio = studio.scalar_one_or_none()
            assert studio.name == 'Акихабара'

    async def test_add_duplicate_studio(self, session, studios):
        with pytest.raises(EntityAlreadyExists):
            await StudioService().add_studio('Страна огня')

    async def test_get_none_studios(self, session):
        none_studios = await StudioService().get_studios()
        assert [] == none_studios

    async def test_get_studios(self, session, studios):
        studios = await StudioService().get_studios()

        assert studios is not None
        assert len(studios) == 3
        for studio in studios:
            assert studio.name in ['Страна огня', 'Страна воды',
                                   'Страна ветра']

    @pytest.mark.parametrize(
            'studio_id, name, expectation',
            [
                [1, 'Яметте кудасай, ониии-чан!', does_not_raise()],
                [1, '', pytest.raises(ValidationError)],
                [1, 1, pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MIN_LENGTH - 1),
                 pytest.raises(ValidationError)],
                [1, 'А' * (NAME_MAX_LENGTH + 1),
                 pytest.raises(ValidationError)],
                [1, None, pytest.raises(ValidationError)],
                # Already exists.
                [1, 'Страна воды', pytest.raises(EntityAlreadyExists)]
            ]
    )
    async def test_edit_studios(
        self,
        session,
        studios,
        studio_id,
        name,
        expectation
    ):
        with expectation:
            await StudioService().edit_studio(studio_id, name)
            studio = await session.scalar(
                select(Studio).where(Studio.id == studio_id)
            )
            assert studio.name == name

    @pytest.mark.parametrize(
            'studio_id, expectation',
            [
                [1, does_not_raise()]
            ]
    )
    async def test_delete_studio(
        self,
        session,
        studios,
        studio_id,
        expectation
    ):
        with expectation:
            old_name = await StudioService().delete_studio(studio_id)

            studio = await session.scalar(
                select(Studio).where(Studio.id == studio_id)
            )
            assert studio is None
            assert old_name == 'Страна огня'
