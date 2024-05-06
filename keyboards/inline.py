from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def menu_studio_kb(studio_name: str, studio_id: int) -> InlineKeyboardMarkup:
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
                    callback_data=f'deleteStudio_'
                                  f'{studio_name}_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Группы',
                    callback_data=f'listGroupsByStudio_{studio_name}'
                                  f'_{studio_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Индивидуальные занятия',
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
    studio_name: str,
    studio_id: int,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Занятие: Добавить',
                    callback_data=f'call_delete_group_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Занятие: Посмотреть',
                    callback_data=f'call_delete_group_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Занятие: Удалить',
                    callback_data=f'call_delete_group_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
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
                    callback_data=f'selectStudentToGroup_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
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
                    callback_data=f'call_delete_group_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Заметка: Посмотреть',
                    callback_data=f'call_delete_group_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Заметка: Удалить',
                    callback_data=f'call_delete_group_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
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
                    callback_data=f'selectGroupByStudio_{group_name}_{group_id}_'
                                  f'{studio_name}_{studio_id}'
                ),
            ],
        ],
    )
    return kb
