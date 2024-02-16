from database.db_api.group import get_groups
from database.db_api.studio import get_studios
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import WeekDays



async def get_studios_kb(session: AsyncSession):
    studios_kb = InlineKeyboardBuilder()
    studios = await get_studios(session)
    for studio in studios:
        studios_kb.add(InlineKeyboardButton(text=studio.name, callback_data=f"show_studio_{studio.name}"))
    return studios_kb.adjust(2).as_markup()


async def delete_studios_kb(session: AsyncSession):
    studios_kb = InlineKeyboardBuilder()
    studios = await get_studios(session)
    for studio in studios:
        studios_kb.add(InlineKeyboardButton(text=studio.name, callback_data=f"delete_studio_{studio.name}"))
    return studios_kb.adjust(2).as_markup()


async def edit_studios_kb(session: AsyncSession):
    studios_kb = InlineKeyboardBuilder()
    studios = await get_studios(session)
    for studio in studios:
        studios_kb.add(InlineKeyboardButton(text=studio.name, callback_data=f"edit_studio_{studio.name}"))
    return studios_kb.adjust(2).as_markup()


async def get_studios_for_group_kb(session: AsyncSession):
    studios_kb = InlineKeyboardBuilder()
    studios = await get_studios(session)
    for studio in studios:
        studios_kb.add(InlineKeyboardButton(text=studio.name, callback_data=f"select_studio_{studio.name}"))
    return studios_kb.adjust(2).as_markup()


async def create_weekdays_kb():
    keyboard = InlineKeyboardBuilder()
    for day in WeekDays:
        keyboard.add(InlineKeyboardButton(text=day.value, callback_data=f"select_weekday_{day.name}"))
    return keyboard.adjust(2).as_markup()


async def get_groups_for_studio(studio_name, session: AsyncSession):
    keyboard = InlineKeyboardBuilder()
    groups = await get_groups(session, studio_name)
    for group in groups:
        keyboard.add(InlineKeyboardButton(text=group.name, callback_data=f"select_group_{group.name}_{studio_name}"))
    return keyboard.adjust(2).as_markup(one_time_keyboard=True)


async def get_studios_for_group(session: AsyncSession):
    studios_kb = InlineKeyboardBuilder()
    studios = await get_studios(session)
    for studio in studios:
        studios_kb.add(InlineKeyboardButton(text=studio.name, callback_data=f"list_groups_{studio.name}"))
    return studios_kb.adjust(2).as_markup()
