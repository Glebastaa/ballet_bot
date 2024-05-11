from schemas.schedule import ScheduleSchema
from services.studio import StudioService
from services.group import GroupService
from services.student import StudentService
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database.models import WeekDays


async def add_button_to_kb(
        kb, items, action,
        one_time_keyboard=False,
        extra_data="",
        extra_data2: int = "",
):
    if not items:
        return None
    for item in items:
        kb.add(InlineKeyboardButton(
            text=item.name,
            callback_data=f'{action}_{item.name}_{item.id}_'
                          f'{extra_data}_{extra_data2}'))
    return kb.adjust(2).as_markup(one_time_keyboard=one_time_keyboard)


async def show_list_studios_menu(action: str):
    "Buttons with a list of all studios"
    return await add_button_to_kb(
        InlineKeyboardBuilder(), await StudioService().get_studios(), action
    )


async def show_list_groups_for_studio(
        action: str,
        studio_name: str,
        studio_id: int
):
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await GroupService().get_groups(studio_id),
        action,
        extra_data=studio_name,
        extra_data2=studio_id
    )


async def show_list_indiv_for_studio(
    action: str,
    studio_name: str,
    studio_id: int,
):
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await GroupService().get_groups(studio_id, is_individual=True),
        action
    )


async def show_all_students(
    action: str
):
    "Buttons with a list all students"
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await StudentService().get_all_students(),
        action
    )


async def show_students_to_group(
    action: str,
    group_id: int
):
    "Buttons with a list student at a group"
    return await add_button_to_kb(
        InlineKeyboardBuilder(),
        await StudentService().get_students_from_group(group_id),
        action
    )


async def show_list_schedules_to_group(
    action: str,
    schedules: list[ScheduleSchema]
):
    keyboard = InlineKeyboardBuilder()
    for schedule in schedules:
        keyboard.add(InlineKeyboardButton(
                text=f'{schedule.start_date.value} : {schedule.start_time}',
                callback_data=f'{action}_{schedule.start_date.value}_'
                              f'{schedule.start_time}_{schedule.id}_'
                              f'{schedule.group_id}'
        ))
    return keyboard.adjust(2).as_markup()


async def select_weekdays(action: str):
    "Buttons with a list of weekdays"
    keyboard = InlineKeyboardBuilder()
    for day in WeekDays:
        keyboard.add(InlineKeyboardButton(
            text=day.value,
            callback_data=f'{action}_{day.value}')
        )
    return keyboard.adjust(2).as_markup()
