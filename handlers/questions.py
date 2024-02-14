from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F
from utils.states import Studio
from database.servise import add_studio

router = Router()


@router.message(F.text.lower() == "добавить студию")
async def form_add_studio(message: Message, state: FSMContext):
    await state.set_state(Studio.name)
    await message.answer("Введите название студии")


@router.message(Studio.name)
async def form_name_studio(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    studio_name = message.text
    result = await add_studio(studio_name)
    if result:
        await message.answer(f"Студия {studio_name} уже существует или произошла ошибка")
    else:
        await message.answer(f"Студия {studio_name} успешно добавлена")
    await state.clear()
