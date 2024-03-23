from functools import wraps
from typing import List

from aiogram.types import Message

from database.models import UserRoles
from services.user import UserService


user_service = UserService()


def registered_user_required(func):
    @wraps(func)
    async def wrapped(message: Message, *args, **kwargs):
        if not await user_service.get_user_by_id(message.from_user.id):
            await message.answer(
                'Для работы с ботом необходимо зарегистрироваться! '
                'Напишите /start для регистрации.'
            )
            return

        state = kwargs.get('state')
        if state:
            return await func(message, state, *args)
        else:
            return await func(message, *args, **kwargs)
    return wrapped


def roles_user_required(allowed_roles: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapped(message: Message):
            user_id = message.from_user.id
            user_role = await user_service.get_user_by_id(telegram_id=user_id)
            if user_role.role.value not in allowed_roles:
                await message.answer(
                    'У вас нет прав для выполнения этой команды!'
                    'Если это ошибка, обратитесь к руководителю студии'
                )
                return
            return await func(message)
        return wrapped
    return decorator
