from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить студию"),
            KeyboardButton(text="Добавить группу"),
        ],
        [
            KeyboardButton(text="Добавить ученика"),
            KeyboardButton(text="Добавить индив"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из меню",
)

main_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список студий"),
            KeyboardButton(text="Список групп в выбранной студии"),
        ],
        [
            KeyboardButton(text="Список учеников в выбранной группе"),
            KeyboardButton(text="Хз-хз"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из меню",
)

main_delete = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Удалить студию"),
            KeyboardButton(text="Удалить группу"),
        ],
        [
            KeyboardButton(text="Удалить ученика"),
            KeyboardButton(text="Удалить индив"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из меню",
)
