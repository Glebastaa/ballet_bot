import asyncio
import logging

from handlers import commands, messages
from handlers.callbacks import callback_router
from handlers.state_handlers import state_router
from aiogram import Bot, Dispatcher
from config import settings


# Запуск бота
async def main():
    bot = Bot(settings.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        messages.router,
        state_router.router,
        callback_router.router,
        commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
