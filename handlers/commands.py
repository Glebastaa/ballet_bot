from aiogram import types, Router
from aiogram.filters import Command, CommandObject


from keyboards import reply

router = Router()


@router.message(Command("add"))
async def add_studio(message: types.Message):
    await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main)
