from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

studio = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить имя студии")
        ],
        [
            InlineKeyboardButton(text="Удалить студию", callback_data="delete_studio")
        ]
    ],
    
)
