from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.db import async_session_maker


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, dict[str, Any]], Awaitable[Any]
            ],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            data['session'] = session
            return await handler(event, data)
