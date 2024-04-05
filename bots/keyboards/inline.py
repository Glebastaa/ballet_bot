from datetime import time
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_studio_kb(studio_name: str, studio_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить имя студии',
                    callback_data=f'call_edit_studio_{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Удалить студию',
                    callback_data=f'call_delete_studio_'
                                  f'{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Список групп',
                    callback_data=f'call_list_group_{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Список индивидуальных занятий',
                    callback_data=f'call_indiv_studio_{studio_name}_'
                                  f'{studio_id}'
                )
            ],
        ],
    )
    return kb


def select_group_for_studio_kb(
        group_name: str,
        group_id: int,
        studio_name: str | None,
        studio_id: int | None,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Добавить занятие в группу',
                    callback_data=(
                        f'call_add_shedule_{group_name}_{group_id}_'
                        f'{studio_id}_{studio_name}'
                    )
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Список занятий в группе',
                    callback_data=(
                        f'call_show_schedule_{group_name}_{group_id}'
                    )
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Сменить имя группы',
                    callback_data=(
                        f'call_edit_group_{group_name}_'
                        f'{group_id}_{studio_name}'
                    )
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить группу',
                    callback_data=f'call_delete_group_{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Добавить ученика в группу',
                    callback_data=f'call_add_student_{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Список учеников',
                    callback_data=f'call_list_students_{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить ученика из группы',
                    callback_data=f'call_delete_student_'
                                  f'{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Добавить/Редактировать заметку для группы',
                    callback_data=f'call_addgroup_notes_'
                                  f'{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Посмотреть заметки в группе',
                    callback_data=f'call_showgroup_notes_'
                                  f'{group_name}_{group_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить заметки в группе',
                    callback_data=f'call_deletegroup_notes_'
                                  f'{group_name}_{group_id}'
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
                    callback_data=f'call_edit_student_'
                                  f'{student_name}_{student_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Удалить ученика',
                    callback_data=(
                        f'call_fulldelete_student_{student_name}_{student_id}'
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Список групп, в которых, состоит ученик',
                    callback_data=f'call_show_group_'
                                  f'{student_name}_{student_id}'
                ),
            ],
        ],
    )
    return kb


def select_schedule_for_group_kb(
        start_date: str,
        start_time: time,
        schedule_id: int,
        group_id: int | None
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'Редактировать рассписание {start_date}:'
                         f'{start_time}',
                    callback_data=f'call_editgroup_schedule_{start_date}_'
                                  f'{start_time}_{schedule_id}_{group_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text=f'Удалить рассписание {start_date}:'
                         f'{start_time}',
                    callback_data=f'call_deletegroup_schedule_{start_date}_'
                                  f'{start_time}_{schedule_id}_{group_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Добавить ученика',
                    callback_data=f'call_student_indiv_{start_date}_'
                                  f'{start_time}_{schedule_id}_{group_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Список учеников',
                    callback_data=f'call_showstudents_indiv_{start_date}_'
                                  f'{start_time}_{schedule_id}_{group_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Удалить ученика',
                    callback_data=f'call_deletestudent_indiv_{start_date}_'
                                  f'{start_time}_{schedule_id}_{group_id}'
                )
            ],
        ]
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
                    callback_data=f'call_delete_student_'
                                  f'{group_name}_{group_id}'
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
