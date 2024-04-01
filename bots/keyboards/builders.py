from schemas.schedule import ScheduleSchema
from schemas.user import UserSchema
from services.studio import StudioService
from services.group import GroupService
from services.student import StudentService
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database.models import UserRoles, WeekDays


async def add_button_to_kb(
        kb, items, action, one_time_keyboard=False,
        extra_data='', extra_data2=1,
):
    if not items:
        return None

    for item in items:
        kb.add(InlineKeyboardButton(
            text=item.name,
            callback_data=(
                f'call_{action}_{item.name}_{item.id}_'
                f'{extra_data}_{extra_data2}'
            )
        ),
        )
    return kb.adjust(2).as_markup(one_time_keyboard=one_time_keyboard)


async def show_list_studios_menu(action: str):
    return await add_button_to_kb(
        InlineKeyboardBuilder(), await StudioService().get_studios(), action
    )


async def show_list_groups_menu(action: str, studio_name: str, studio_id: int):
    return await add_button_to_kb(
        InlineKeyboardBuilder(), await GroupService().get_groups(studio_id),
        action=action,
        extra_data=studio_name,
        extra_data2=studio_id
    )


async def process_show_group_for_student(student_id: int, student_name: str):
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await GroupService().get_groups_from_student(
            student_id, is_individual=False
        ),
        'pick_groups',
        extra_data=student_name,
        extra_data2=student_id
    )


async def show_list_students_menu(action: str):
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await StudentService().get_all_students(),
        action,
    )


async def show_list_students_from_group_menu(action: str, group_id: int):
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await StudentService().get_students_from_group(group_id),
        action,
    )


async def process_select_weekdays(action: str):
    keyboard = InlineKeyboardBuilder()
    for day in WeekDays:
        keyboard.add(InlineKeyboardButton(
            text=day.value, callback_data=f'{action}_{day.value}')
        )
    return keyboard.adjust(2).as_markup()


async def show_list_indiv_menu(action: str, studio_name: str, studio_id: int):
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await GroupService().get_groups(studio_id, is_individual=True),
        action,
        extra_data=studio_name,
        extra_data2=studio_id
    )


async def show_users_for_role(users: list[UserSchema], role: str):
    keyboard = InlineKeyboardBuilder()
    for user in users:
        keyboard.add(InlineKeyboardButton(
            text=user.username,
            callback_data=f'show_users_to_{user.username}_{user.id}'
        ))
    return keyboard.adjust(1).as_markup()


async def switch_to_role_kb(
    action: str, user_name: str | None, user_id: int | None
):
    keyboard = InlineKeyboardBuilder()
    for role in UserRoles:
        keyboard.add(InlineKeyboardButton(
            text=role.value,
            callback_data=f'{action}_{role.value}_{user_name}_{user_id}'
        ))
    return keyboard.adjust(1).as_markup()


async def show_list_schedules_for_group(
        action: str,
        schedules: list[ScheduleSchema]
):
    keyboard = InlineKeyboardBuilder()
    for schedule in schedules:
        keyboard.add(InlineKeyboardButton(
            text=f'{schedule.start_date.value}, {schedule.start_time}',
            callback_data=f'{action}_{schedule.start_date.value}_'
                          f'{schedule.start_time}_{schedule.id}'
        ))
    return keyboard.adjust(2).as_markup()
