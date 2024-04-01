from datetime import time
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.group import GroupService
from bots.keyboards import inline, builders


router = Router()
group_service = GroupService()

schedule_list = [
    'group_schedule', 'deletegroup_schedule', 'editgroup_schedule',
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
    message = callback.message

    if action == 'group_schedule':
        keyboard = inline.select_schedule_for_group_kb(
            start_date, start_time, schedule_id
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
