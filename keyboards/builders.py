from services.studio import StudioService
from services.group import GroupService
from services.student import StudentService
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database.models import WeekDays


async def add_button_to_kb(
        kb, items, action, one_time_keyboard=False, extra_data=""
):
    if not items:
        return None
    for item in items:
        kb.add(InlineKeyboardButton(
            text=item.name,
            callback_data=f'{action}_{item.name}_{item.id}_{extra_data}')
        )
    return kb.adjust(2).as_markup(one_time_keyboard=one_time_keyboard)


async def show_list_studios_menu(action: str):
    return await add_button_to_kb(
        InlineKeyboardBuilder(), await StudioService().get_studios(), action
    )


async def select_weekdays(action: str):
    keyboard = InlineKeyboardBuilder()
    for day in WeekDays:
        keyboard.add(InlineKeyboardButton(
            text=day.value,
            callback_data=f'{action}_{day.value}')
        )
    return keyboard.adjust(2).as_markup()


async def show_list_groups_for_studio(studio_name, studio_id):
    return await add_button_to_kb(InlineKeyboardBuilder(), await GroupService().get_groups(studio_id), 'selectGroupByStudio', extra_data=studio_name)


async def process_edit_group_name(studio_name, studio_id):
    return await add_button_to_kb(InlineKeyboardBuilder(), await GroupService().get_groups(studio_id), "edit_group", extra_data=studio_name)


async def show_list_students_menu():
    return await add_button_to_kb(InlineKeyboardBuilder(), await StudentService().get_all_students(), "pick_student")


async def process_add_student_to_group():
    return await add_button_to_kb(InlineKeyboardBuilder(), await StudentService().get_all_students(), "add_student2")


async def show_student_to_group_menu(group_id):
    return await add_button_to_kb(InlineKeyboardBuilder(), await StudentService().get_students_from_group(group_id), "pick_student")
