from database.models import UserRoles
from exceptions import SameRoleError, UserAlreadyExistsError
from logger_config import setup_logger
from schemas.user import UserSchema, UserSchemaAdd, UserSchemaUpdateRole
from utils.unitofwork import UnitOfWork


logger = setup_logger('user')


class UserService:
    def __init__(self) -> None:
        self.uow: UnitOfWork = UnitOfWork()

    async def _is_already_exists(
            self,
            telegram_id: int,
            username: str,
            uow: UnitOfWork
    ) -> None:
        id_check = await uow.user.get_all(id=telegram_id)
        name_check = await uow.user.get_all(username=username)
        if id_check or name_check:
            logger.error(
                f'Пользователь "{telegram_id}" уже существует. '
                f'Либо существует юзернейм "{username}".'
            )
            raise UserAlreadyExistsError(
                {'telegram_id': telegram_id,
                 'username': username}
            )

    async def register_user(
            self,
            telegram_id: int,
            username: str
    ) -> UserSchema:
        """Add a user to db."""
        validated_data = UserSchemaAdd(
            id=telegram_id,
            username=username,
            role=UserRoles.VISITOR
        )
        async with self.uow:
            await self._is_already_exists(telegram_id, username, self.uow)
            user = await self.uow.user.add(validated_data.model_dump())
            await self.uow.commit()
            logger.info(
                f'Пользователь "{telegram_id}" - "{username}" '
                'добавлен как посетитель.'
            )
            return user.to_read_model(UserSchema)

    async def switch_to_another_role(
            self,
            telegram_id: int,
            role: UserRoles
    ) -> UserSchema:
        """Change a role."""
        role_in = UserSchemaUpdateRole(role=role)
        async with self.uow:
            user_check = await self.uow.user.get(id=telegram_id)
            if user_check.role == role:
                raise SameRoleError(role.value)
            user = await self.uow.user.update(
                data=role_in.model_dump(),
                id=telegram_id
            )
            await self.uow.commit()
            logger.info(
                f'Роль пользователя "{telegram_id}" - '
                f'"{user.username}" изменена на "{user.role.value}".'
            )
            return user.to_read_model(UserSchema)

    async def get_visitors(
            self
    ) -> list[UserSchema]:
        """Gets all visitors."""
        async with self.uow:
            visitors = await self.uow.user.get_all(role=UserRoles.VISITOR)
            return [visitor.to_read_model(UserSchema) for visitor in visitors]

    async def delete_all_visitors(self) -> None:
        """Remove all visitors from db."""
        async with self.uow:
            await self.uow.user.delete_all(
                {'role': UserRoles.VISITOR}
            )
            logger.info('БД очищена от посетителей.')
            await self.uow.commit()

    async def get_users_by_role(self, role: UserRoles) -> list[UserSchema]:
        """Gets all users by roles."""
        UserSchemaUpdateRole(role=role)  # some validation.
        async with self.uow:
            users = await self.uow.user.get_all(role=role)
            return [user.to_read_model(UserSchema) for user in users]

    async def delete_user(self, telegram_id: int) -> UserSchema:
        """Delete a user from db."""
        async with self.uow:
            user = await self.uow.user.delete(id=telegram_id)
            await self.uow.commit()
            logger.info(
                f'Пользователь "{telegram_id}" - "{user.username}" удален.'
            )
            return user.to_read_model(UserSchema)

    async def get_user_by_id(self, telegram_id: int) -> UserSchema | None:
        """Gets a user by telegram id or None."""
        async with self.uow:
            user = await self.uow.user.get_all(id=telegram_id)
            if not user:
                return None
            return user[0].to_read_model(UserSchema)

    async def get_user_id_by_username(self, username: str) -> int | None:
        """Gets id by username or None."""
        async with self.uow:
            user = await self.uow.user.get_all(username=username)
            return user[0].id if user else None
