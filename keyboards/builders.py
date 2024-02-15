from database.servise import get_studios
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession


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