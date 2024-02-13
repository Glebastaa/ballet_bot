import asyncio
from aiogram import Bot, Dispatcher
import logging

from handlers import bot_messages, commands, questions

from config import config

logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        commands.router,
        bot_messages.router,
        questions.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
