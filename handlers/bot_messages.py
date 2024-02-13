from aiogram import Router, F, types

router = Router()


@router.message(F.text.lower() == "добавить студию")
async def add_studio(message: types.Message):
    await message.reply("Напишите название студии")


@router.message(F.text.lower() == "добавить группу")
async def add_group(message: types.Message):
    await message.reply("Напишите название группы")


@router.message(F.text.lower() == "добавить ученика")
async def add_student(message: types.Message):
    await message.reply("Напишите имя ученика")


@router.message(F.text.lower() == "добавить индив")
async def add_indiv(message: types.Message):
    await message.reply("Выберите имя ученика для индива")
