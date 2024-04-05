from datetime import time
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.group import GroupService
from services.student import StudentService
from bots.keyboards import inline, builders


router = Router()
group_service = GroupService()
student_service = StudentService()

schedule_list = [
    'group_schedule', 'deletegroup_schedule', 'editgroup_schedule',
    'indiv_schedule', 'student_indiv', 'deletestudent_indiv',
    'showstudents_indiv', 'delete_indiv'
]


async def schedule_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext | None = None
) -> None:
    """Manage callback requests related to schedule."""
    start_date: str = callback.data.split('_')[3]
    start_time: time = callback.data.split('_')[4]  # type: ignore
    schedule_id = int(callback.data.split('_')[5])
    group_id = int(callback.data.split('_')[6])
    message = callback.message

    if action == 'group_schedule':
        keyboard = inline.select_schedule_for_group_kb(
            start_date, start_time, schedule_id, group_id
        )
        await message.edit_text('Выберите действие:')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'deletegroup_schedule':
        await group_service.delete_schedule(schedule_id)
        await message.edit_text('Расписание успешно удалено')
        await message.edit_reply_markup(reply_markup=None)

    elif action == 'editgroup_schedule':
        keyboard = await builders.process_select_weekdays('date_schedule')
        await state.update_data(schedule_id=schedule_id)
        await message.edit_text('Выберите день недели:')
        await message.edit_reply_markup(reply_markup=keyboard)  # type: ignore

    elif action == 'student_indiv':
        students = await student_service.get_all_students()
        if students:
            keyboard = await builders.show_list_students_menu(
                'select_studentindiv'
            )
            await state.update_data(
                schedule_id=schedule_id,
                group_id=group_id,
                start_date=start_date,
                start_time=start_time,
            )
            await message.edit_text(
                f'Выберите ученика для добавление в рассписание {start_date}:'
                f'{start_time}'
            )
            await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'deletestudent_indiv':
        students = await student_service.get_students_from_group(group_id)
        if students:
            keyboard = await builders.show_list_students_from_group_menu(
                'delete_studentindiv',
                group_id
            )
            await state.update_data(
                schedule_id=schedule_id,
                group_id=group_id,
                start_date=start_date,
                start_time=start_time,
            )
            await message.edit_text(
                f'Выберите ученика для удаления из индива в {start_date}:'
                f'{start_time}'
            )
            await message.edit_reply_markup(reply_markup=keyboard)
        else:
            await message.edit_text(
                'Учеников нету'
            )

    elif action == 'showstudents_indiv':
        students = await student_service.get_students_from_group(group_id)
        if students:
            keyboard = await builders.show_list_students_from_group_menu(
                'trash',
                group_id
            )
            await message.edit_text('Вот кто тут есть')
            await message.edit_reply_markup(reply_markup=keyboard)
        else:
            await message.edit_text(
                'Учеников нету'
            )

    elif action == 'delete_indiv':
        await group_service.delete_group(group_id)
        await message.edit_text(
            f'Индив {start_date}:{start_time} успешно удалена'
        )
        await message.edit_reply_markup(reply_markup=None)
