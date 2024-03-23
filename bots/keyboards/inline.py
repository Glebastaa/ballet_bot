from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_studio_kb(studio_name: str, studio_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить имя студии',
                    callback_data=f'edit_studio_{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Удалить студию',
                    callback_data=f'delete_studio_{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Список групп',
                    callback_data=f'list_group_{studio_name}_{studio_id}'
                )
            ]
        ],
    )
    return kb


def select_group_for_studio_kb(
        group_name: str,
        group_id: int,
        studio_name: str,
        studio_id: int,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Сменить имя группы',
                    callback_data=(
                        f'edit_group_{group_name}_{group_id}_{studio_name}'
                    )
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Добавить занятие в группу',
                    callback_data=(
                        f'add_shedule_{group_name}_{group_id}_'
                        f'{studio_id}_{studio_name}'
                    )
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить группу',
                    callback_data=f'delete_group_{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Добавить ученика в группу',
                    callback_data=f'add_student_{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить ученика из группы',
                    callback_data=f'delete_student_{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Список учеников',
                    callback_data=f'list_students_{group_name}_{group_id}'
                ),
            ],
        ],
    )
    return kb


def select_students_kb(
    student_name: str,
    student_id: int
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить имя ученика',
                    callback_data=f'edit_student_{student_name}_{student_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить ученика',
                    callback_data=(
                        f'fulldelete_student_{student_name}_{student_id}'
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Список групп, в которых, состоит ученик',
                    callback_data=f'show_group_{student_name}_{student_id}'
                ),
            ],
        ],
    )
    return kb


def select_student_for_group_kb(
        group_name: str,
        group_id: int,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'Удалить ученика из группы {group_name}',
                    callback_data=f'delete_student_{group_name}_{group_id}'
                ),
            ],
        ],
    )
    return kb


def show_admin_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Выдать роль пользователю',
                    callback_data='switch_to_role'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Увидеть всех пользователей с ролью',
                    callback_data='show_users_role'
                )
            ],
        ]
    )
    return kb


def show_users_role_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Показать всех Владельцев',
                    callback_data='show_role_owner'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Показать всех Учителей',
                    callback_data='show_role_teacher'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Показать всех Учеников',
                    callback_data='show_role_student'
                ),
            ],
        ],
    )
    return kb


def show_user_menu_kb(user_name: str, user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить роль',
                    callback_data=f'change_role_{user_name}_{user_id}'
                ),
            ],
        ],
    )
    return kb
