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
            KeyboardButton(text="Список групп"),
        ],
        [
            KeyboardButton(text="Список учеников"),
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

main_edit = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Изменить имя студии"),
            KeyboardButton(text="Изменить имя группы"),
        ],
        [
            KeyboardButton(text="Изменить имя ученика"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите кнопку из меню",
)
