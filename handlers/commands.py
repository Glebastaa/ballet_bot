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
