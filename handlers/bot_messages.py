from audioop import add
from aiogram import Router, F, types
from keyboards import builders


router = Router()


@router.message(F.text.lower() == "список студий")
async def message_list_studios(message: types.Message):
    await message.reply("Список студий:", reply_markup=await builders.get_studios_kb())


@router.message(F.text.lower() == "удалить студию")
async def message_delete_studio(message: types.Message):
    await message.reply("Выберите студию для удаления:", reply_markup=await builders.delete_studios_kb())
