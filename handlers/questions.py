import time
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import builders
from database.models import WeekDays
from database.db_api.studio import add_studio
from database.db_api.group import add_group, edit_group
from utils.states import Studio, Group, EditGroup
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

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


@router.message(Group.start_time)
async def form_end_add_group(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(start_time=message.text)
    data = await state.get_data()
    group_name = data.get("group_name")
    studio_name = data.get("studio_name")
    start_date = data.get("start_date")
    start_time_str = message.text
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    await add_group(session, group_name, studio_name, start_time, start_date)
    await message.answer(f"Группа {group_name} успешно добавлена в студию {studio_name} с временем начала в {start_date} : {start_time}")
    await state.clear()


@router.message(EditGroup.new_group_name)
async def form_new_group_name(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(new_group_name=message.text)
    data = await state.get_data()
    group_name = data.get("group_name")
    new_group_name = data.get("new_group_name")
    studio_name = data.get("studio_name")
    await edit_group(session, group_name, new_group_name, studio_name)
    await message.answer(f"Группа {group_name} успешно изменена на {new_group_name}")
    await state.clear()
