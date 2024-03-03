from typing import Type
from database.models import UserRoles
from exceptions import UserAlreadyExistsError
from schemas.user import UserSchema, UserSchemaAdd, UserSchemaUpdateRole
from utils.unitofwork import UnitOfWork


class UserService:
    def __init__(self) -> None:
        self.uow: Type[UnitOfWork] = UnitOfWork()

    async def _is_already_exists(
            self,
            telegram_id: int,
            username: str,
            uow: Type[UnitOfWork]
    ) -> None:
        id_check = await uow.user.get(telegram_id)
        name_check = await uow.user.get_all({'username': username})
        if id_check or name_check:
            raise UserAlreadyExistsError(
                {'telegram_id': telegram_id,
                 'username': username}
            )

    async def register_user(
            self,
            telegram_id: int,
            username: str
    ) -> UserSchema:
        """Add user to db."""
        validated_data = UserSchemaAdd(
            id=telegram_id,
            username=username,
            role=UserRoles.VISITOR
        )
        async with self.uow:
            await self._is_already_exists(telegram_id, username, self.uow)
            user = await self.uow.user.add(validated_data.model_dump())
            await self.uow.commit()
            return user.to_read_model(UserSchema)

    async def switch_to_another_role(
            self,
            telegram_id: int,
            role: UserRoles
    ) -> UserSchema:
        """Change role."""
        role = UserSchemaUpdateRole(role=role)
        async with self.uow:
            user = await self.uow.user.update(telegram_id, role.model_dump())
            await self.uow.commit()
            return user.to_read_model(UserSchema)

    async def get_visitors(
            self
    ) -> list[UserSchema]:
        """Get list of visitors."""
        async with self.uow:
            visitors = await self.uow.user.get_all(
                {'role': UserRoles.VISITOR}
            )
            return [visitor.to_read_model(UserSchema) for visitor in visitors]

    async def delete_all_visitors(self) -> None:
        """Remove all visitors from db."""
        async with self.uow:
            await self.uow.user.delete_all(
                {'role': UserRoles.VISITOR}
            )
            await self.uow.commit()

    async def get_users_by_role(self, role: UserRoles) -> list[UserSchema]:
        """Get list of users by they roles."""
        UserSchemaUpdateRole(role=role)  # some validation.
        async with self.uow:
            users = await self.uow.user.get_all(
                {'role': role}
            )
            return [user.to_read_model(UserSchema) for user in users]

    async def delete_user(self, telegram_id: int) -> UserSchema:
        """Delete user from db."""
        async with self.uow:
            user = await self.uow.user.delete(telegram_id)
            await self.uow.commit()
            return user.to_read_model(UserSchema)
