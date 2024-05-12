from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def menu_studio_kb(studio_name: str, studio_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Изменить имя студии',
                    callback_data=f'editStudio_{studio_name}_{studio_id}'
                ),
                InlineKeyboardButton(
                    text='Удалить студию',
                    callback_data=f'deleteStudio_'
                                  f'{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Добавить группу',
                    callback_data=f'addGroupBySelectStudio_{studio_name}'
                                  f'_{studio_id}'
                ),
                InlineKeyboardButton(
                    text='Группы',
                    callback_data=f'listGroupsByStudio_{studio_name}'
                                  f'_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Добавить индив',
                    callback_data=f'addIndiv_{studio_name}_'
                                  f'{studio_id}'
                ),
                InlineKeyboardButton(
                    text='Индивидуальные занятия',
                    callback_data=f'listIndiv_{studio_name}_'
                                  f'{studio_id}'
                )
            ],
        ],
    )
    return kb


def select_schedule_to_studio_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Добавить ученика',
                    callback_data='selectStudentToIndiv'
                ),
                InlineKeyboardButton(
                    text='Посмотреть учеников',
                    callback_data='showStudentsToIndiv'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Удалить ученика',
                    callback_data='delStudentToIndiv'
                ),
                InlineKeyboardButton(
                    text='Удалить индив',
                    callback_data='deleteIndiv'
                ),
            ],
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
                    text='Занятие: Добавить',
                    callback_data=f'addScheduleGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Занятие: Посмотреть',
                    callback_data=f'showScheduleGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Занятие: Удалить',
                    callback_data=f'deleteScheduleGroup_{group_name}_'
                                  f'{group_id}_{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Группа: Сменить имя',
                    callback_data=f'editGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Группа: Удалить',
                    callback_data=f'deleteGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Ученик: Добавить',
                    callback_data=f'selectStudentToGroup_{group_name}_'
                                  f'{group_id}_{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Ученик: Посмотреть',
                    callback_data=f'showStudentToGroup_{group_name}_'
                                  f'{group_id}_{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Ученик: Удалить',
                    callback_data=f'deleteStudentToGroup_{group_name}_'
                                  f'{group_id}_{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Заметка: Добавить/Редактировать',
                    callback_data=f'addNotesToGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Заметка: Посмотреть',
                    callback_data=f'showNotesToGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Заметка: Удалить',
                    callback_data=f'deleteNotesGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
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
                    text='Ученик: Редактировать',
                    callback_data=f'editStudent_{student_name}_{student_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Ученик: Удалить',
                    callback_data=f'deleteStudent_{student_name}_{student_id}'
                ),
            ],
        ],
    )
    return kb


def back_to_group_menu(
    group_name: str,
    group_id: int,
    studio_name: str,
    studio_id: int,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Вернутся назад',
                    callback_data=f'selectGroupByStudio_{group_name}_'
                                  f'{group_id}_{studio_name}_{studio_id}'
                ),
            ],
        ],
    )
    return kb


def back_to_indiv_menu(
    start_date: str,
    start_time: str,
    schedule_id: int,
    group_id: int
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Вернутся назад',
                    callback_data=f'menuIndiv_{start_date}_{start_time}_'
                                  f'{schedule_id}_{group_id}'
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
                    callback_data='changeRole'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Увидеть всех пользователей с ролью',
                    callback_data='showUsersRole'
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
                    callback_data='showRole_owner'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Показать всех Учителей',
                    callback_data='showRole_teacher'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Показать всех Учеников',
                    callback_data='showRole_student'
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
                    callback_data=f'switchRole_{user_name}_{user_id}'
                ),
            ],
        ],
    )
    return kb
