from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import get_studios


def show_studios():
    studios = get_studios()
    # Тут блять должны быть кнопки с именами студии
        