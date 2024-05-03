from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_studio_kb(studio_name: str, studio_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить имя студии',
                    callback_data=f'editStudio_{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Удалить студию',
                    callback_data=f'deleteStudio_{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Список групп',
                    callback_data=f'listGroupsByStudio_'
                                  f'{studio_name}_{studio_id}'
                )
            ]
        ],
    )
    return kb


def select_group_for_studio_kb(group_name: str, group_id: int, studio_name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Сменить имя группы", callback_data=f"edit_group_{group_name}_{group_id}_{studio_name}"),
                InlineKeyboardButton(text="Удалить группу", callback_data=f"delete_group_{group_name}_{group_id}")
            ],
            [
                InlineKeyboardButton(text="Добавить ученика в группу", callback_data=f"add_student_{group_name}_{group_id}"),
                InlineKeyboardButton(text="Список учеников", callback_data=f"list_students_{group_name}_{group_id}")
            ],
        ],
    )
    return kb


def select_students_kb(student_name: str, student_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить имя ученика", callback_data=f"edit_student_{student_name}_{student_id}")
            ],
            [
                InlineKeyboardButton(text="Удалить ученика", callback_data=f"delete_student_{student_name}_{student_id}")
            ],
            [
                InlineKeyboardButton(text="Список групп, в которых состоит ученик", callback_data=f"list_students_{student_name}_{student_id}")
            ]
        ],
    )
    return kb
