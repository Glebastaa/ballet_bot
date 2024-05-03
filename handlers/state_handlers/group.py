from datetime import datetime, time
import re

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.models import WeekDays
from handlers.commands import add_main, delete_main, edit_main, show_main
from schemas.group import GroupSchema
from services.group import GroupService
from exceptions import EntityAlreadyExists, ScheduleTimeInsertionError
from utils.states import AddGroup
from keyboards import builders


router = Router()
group_service = GroupService()


async def handle_failure(
        message: Message,
        state: FSMContext,
        fail_count: int,
        error_message: str
):
    fail_count += 1
    if fail_count >= 3:
        await message.answer(
            'У вас закончились попытки. Пожалуйста, попробуйте еще раз позже.'
        )
        await state.clear()
        return True
    await state.update_data(fail_count=fail_count)
    await message.answer(error_message)
    return False


@router.message(AddGroup.name)
async def step2_add_group(message: Message, state: FSMContext):
    "Step 2. Check and add to state group name"
    group_name: str = message.text
    kb = await builders.select_weekdays('weekdayGroup')
    data = await state.get_data()
    studio_id: int = data.get('studio_id')

    if re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', group_name):
        try:
            group = await group_service.add_group(
                group_name, studio_id
            )
            await state.update_data(group=group, group_name=group_name)
            await message.answer(
                'Выберите день, когда будет проходить '
                f'занятии в группе {group_name}',
                reply_markup=kb
            )
        except EntityAlreadyExists:
            await message.answer(
                f'Группа {group_name} уже существует. '
                'Попробуйте ввести другое название.'
            )

    else:
        await message.answer(
            'Пожалуйста, введите имя группы корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(AddGroup.start_time)
async def step4_add_group(message: Message, state: FSMContext):
    "Step 4. Check start_time and add schedule to group"
    start_time_str = str(message.text)
    data = await state.get_data()
    studio_name: str = data.get('studio_name')
    start_date: WeekDays = data.get('start_date')
    group_name: str = data.get('group_name')
    group: GroupSchema = data.get('group')
    fail_count: int = data.get('fail_count', 0)

    if start_time_str == '/add':
        return await add_main(message)
    elif start_time_str == '/show':
        return await show_main(message)
    elif start_time_str == '/delete':
        return await delete_main(message)
    elif start_time_str == '/edit':
        return await edit_main(message)

    try:
        await group_service.add_schedule_to_group(
            group_id=group.id,
            start_time=datetime.strptime(start_time_str, '%H:%M').time(),
            start_date=start_date
        )
        await message.answer(
            f'Добавлено расписание день - {start_date.value}, время - '
            f'{start_time_str} для группы {group_name} в студии {studio_name}'
        )
        await state.clear()
    except ValueError:
        if await handle_failure(
            message, state, fail_count,
            'Время введено неверно. Пожалуйста, введите время в формате HH:MM.'
        ):
            return
    except ScheduleTimeInsertionError:
        if await handle_failure(
            message, state, fail_count,
            f'Невозможно добавить расписание. Время {start_time_str} уже '
            'занято или слишком близко к существующему расписанию.'
        ):
            return
