from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import reply, builders

router = Router()


@router.message(Command("main"))
async def add_main(message: Message):
    await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main)


#@router.message()
#async def echo(message: Message):
    #msg = message.text.lower()

    #if msg == "main":
        #await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main)
    #else:
        #await message.answer("Я не понимаю, что вы пишете. Для работы с ботом нажмите 'Меню' и выберите, то, что вам надо")
