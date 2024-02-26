import asyncio
import logging

from handlers import bot_messages, commands, questions
from callbacks import callbacks
from middlewares.database import DatabaseMiddleware
from aiogram import Bot, Dispatcher
from config import settings


# Запуск бота
async def main():
    bot = Bot(settings.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.update.middleware(DatabaseMiddleware())

    dp.include_routers(
        bot_messages.router,
        questions.router,
        callbacks.router,
        commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("ТЫ БЛЯТЬ ВЫШЕЛ")
