from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import reply

router = Router()


@router.message(Command("add"))
async def add_main(message: Message):
    await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main)


@router.message(Command("show"))
async def show_main(message: Message):
    await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_info)



@router.message(Command("delete"))
async def delete_main(message: Message):
    await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_delete)



@router.message(Command("edit"))
async def edit_main(message: Message):
    await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_edit)


@router.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "add":
        await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main)
    elif msg == "show":
        await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_info)
    elif msg == "delete":
        await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_delete)
    elif msg == "edit":
        await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_edit)
    else:
        await message.answer("Я не понимаю, что вы пишете. Для работы с ботом нажмите 'Меню' и выберите, то, что вам надо")
