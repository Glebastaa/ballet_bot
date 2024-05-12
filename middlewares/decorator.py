from functools import wraps

from aiogram.types import Message

from services.user import UserService


user_service = UserService()


def registered_user_required(func):
    "User registration verification decorator"
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


def roles_user_required(allowed_roles: list[str]):
    "User role verification decorator"
    def decorator(func):
        @wraps(func)
        async def wrapped(message: Message, *args, **kwargs):
            curr_id = message.from_user.id
            curr_role = await user_service.get_user_by_id(telegram_id=curr_id)
            if curr_role.role.value not in allowed_roles:
                await message.answer(
                    'У вас нет прав для выполнения этой команды! '
                    'Если это ошибка, обратитесь к руководителю студии'
                )
                return
            state = kwargs.get('state')
            if state:
                return await func(message, state, *args)
            else:
                return await func(message, *args, **kwargs)
        return wrapped
    return decorator
