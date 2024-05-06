from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить студию"),
        ],
        [
            KeyboardButton(text="Студии"),
        ],
        [
            KeyboardButton(text="Добавить ученика"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из меню",
)
