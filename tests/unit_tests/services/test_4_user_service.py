from types import NoneType
from pydantic import ValidationError
import pytest

from contextlib import nullcontext as does_not_raise

from sqlalchemy import select
from database.models import User, UserRoles
from exceptions import UserAlreadyExistsError

from schemas.user import UserSchema
from services.user import UserService


@pytest.mark.user_service
class TestUserService:

    @pytest.mark.parametrize(
            'telegram_id, username, expectation',
            [
                [5013573061, 'Nagibattor888', does_not_raise()],
                [5013573061, 'Андрей Петров', does_not_raise()],
                [5013573061, None, pytest.raises(ValidationError)]
            ]
    )
    async def test_register_new_user(
        self,
        session,
        telegram_id,
        username,
        expectation
    ):
        with expectation:
            user = await UserService().register_user(telegram_id, username)

            test_user = await session.get(User, telegram_id)
            assert test_user.id == user.id
            assert test_user.username == username
            assert test_user.role == UserRoles.VISITOR

    @pytest.mark.parametrize(
            'telegram_id, username, expectation',
            [
                [5013573061, 'Nagibattor888', does_not_raise()],
                [5213573061, 'Андрей Петров',
                 pytest.raises(UserAlreadyExistsError)],
                [5013573061, 'Сасуми Хиросава',
                 pytest.raises(UserAlreadyExistsError)]
            ]
    )
    async def test_register_dublicate_username_or_id(
            self,
            session,
            users,
            telegram_id,
            username,
            expectation
    ):
        with expectation:
            await UserService().register_user(telegram_id, username)

    async def test_switch_to_another_role(self, session, users):
        await UserService().switch_to_another_role(
            5263573061, UserRoles.STUDENT)

        user = await session.get(User, 5263573061)
        assert user.role == UserRoles.STUDENT

    async def test_get_visitors(self, session, users):
        visitors = await UserService().get_visitors()

        assert len(visitors) == 2
        for visitor in visitors:
            assert visitor.username in ['Aiobahn', 'Flow']

    async def test_delete_all_visitors(self, session, users):
        await UserService().delete_all_visitors()

        users = await session.execute(select(User))
        users = users.scalars().all()

        assert len(users) == 4
        for user in users:
            assert user.id not in [5253573061, 5263573061]

    async def test_get_user_by_role(self, session, users):
        students = await UserService().get_users_by_role(UserRoles.STUDENT)
        owner = await UserService().get_users_by_role(UserRoles.OWNER)

        assert len(students) == 2
        assert len(owner)
        for student in students:
            assert student.username in ['Юрима', 'Tommy heavenly6']
        assert owner[0].username == 'Сасуми Хиросава'

    async def test_delete_user(self, session, users):
        user = await UserService().delete_user(5243573061)

        test_user = await session.get(User, 5243573061)
        assert test_user is None
        assert user.username == 'Tommy heavenly6'

    @pytest.mark.parametrize(
            'user_id, expect, expectation',
            [
                [5213573061, UserSchema, does_not_raise()],
                [5213573062, NoneType, does_not_raise()]
            ]
    )
    async def test_get_user_by_id(self, session, users, user_id, expect,
                                  expectation):
        with expectation:
            user = await UserService().get_user_by_id(user_id)
            assert isinstance(user, expect)

    async def test_get_id_by_username(self, session, users):
        user_id = await UserService().get_user_id_by_username(
            'Сасуми Хиросава')
        assert isinstance(user_id, int)
        assert user_id == 5213573061

        none_user = await UserService().get_user_id_by_username('Сасуми')
        assert none_user is None
