from database.servise import get_studios
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton


async def get_studios_kb():
    studios_kb = InlineKeyboardBuilder()
    studios = await get_studios()
    for studio in studios:
        studios_kb.add(InlineKeyboardButton(text=studio.name, callback_data=f"show_studio_{studio.name}"))
    return studios_kb.adjust(2).as_markup()


async def delete_studios_kb():
    studios_kb = InlineKeyboardBuilder()
    studios = await get_studios()
    for studio in studios:
        studios_kb.add(InlineKeyboardButton(text=studio.name, callback_data=f"delete_studio_{studio.name}"))
    return studios_kb.adjust(2).as_markup()
