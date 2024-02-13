from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import Studio, Group
from database import add_studio, get_studios
from keyboards import builders, inline

router = Router()

@router.message(Command("add_studio"))
async def form_add_studio(message: Message, state: FSMContext):
    await state.set_state(Studio.name)
    await message.answer("Введите название студии")


@router.message(Studio.name)
async def form_name_studio(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    studio_name = message.text
    result = add_studio(studio_name)
    if result:
        await message.answer(f"Студия {studio_name} успешно добавлена")
    else:
        await message.answer(f"Студия {studio_name} уже существует или произошла ошибка")
    await state.clear()


@router.message(Command("add_group"))
async def form_add_group(message: Message, state: FSMContext):
    await state.set_state(Group.name)
    await message.answer("Напишите название группы")


@router.message(Group.name)
async def form_studio_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Group.studio_name)
    await message.answer("Выберите студию, в которую хотите добавить группу2")  # Тут блять где-то должен быть reply_markup= на кнопки с именами студии и дальнейшая их запись


@router.message(Group.studio_name)
async def form_name_group(message: Message, state: FSMContext):

    await state.update_data(studio_name=inline.show_studios)
    await state.set_state(Group.start_date)
    await message.answer("Теперь, введите день недели, когда проходи занятие")


@router.message(Group.start_date)
async def form_start_date(message: Message, state: FSMContext):
    await state.update_data(start_date=message.text)
    await state.set_state(Group.start_time)
    await message.answer("Введите время начала занятия")

@router.message(Group.start_time)
async def form_start_time(message: Message, state: FSMContext):
    await state.update_data(start_time=message.text)
    await state.clear()

    formatted_text = []
    for group_name, studio_name, start_date, start_time in get_groups(studio_name):
        formatted_text.append(
            f"Группа {group_name} добавлена к студии {studio_name} с началом занятия {start_date} в {start_time}"
        )
