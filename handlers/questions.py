from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from database.models import WeekDays
from utils.states import Studio, Group
from database.servise import add_studio, add_group
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards import builders

router = Router()


@router.message(Studio.name)
async def form_name_studio(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(name=message.text)
    studio_name = message.text
    result = await add_studio(session, studio_name)
    if result:
        await message.answer(f"Студия {studio_name} уже существует или произошла ошибка")
    else:
        await message.answer(f"Студия {studio_name} успешно добавлена")
    await state.clear()


@router.message(Group.group_name)
async def form_name_group(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(group_name=message.text)
    group_name = message.text
    await state.set_state(Group.studio_name)
    await message.answer(f"Выберите студию для группы {group_name}", reply_markup=await builders.get_studios_for_group_kb(session=session))


@router.message(Group.start_date)
async def form_start_time_group(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(start_date=message.text)
    data = await state.get_data()
    group_name = data.get("group_name")
    await state.set_state(Group.start_time)
    await message.answer(f"Введите время начала занятия для группы {group_name}")


@router.message(Group.start_time)
async def form_end_add_group(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(start_time=message.text)
    data = await state.get_data()
    group_name = data.get("group_name")
    studio_name = data.get("studio_name")
    start_date = data.get("start_date")
    start_time_str = message.text
    start_time = # тут чето преобразовать как-то надэ
    result = await add_group(session, group_name, studio_name, start_time, WeekDays.friday)
    if result:
        await message.answer(f"Группа {group_name} успешно добавлена в студию {studio_name} с временем начала в {start_date} : {start_time}")
    else:
        await message.answer(f"Группа {group_name} уже существует или произошла ошибка")
    await state.clear()
