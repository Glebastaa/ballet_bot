import random
import re
import string
from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.models import WeekDays
from handlers.commands import add_main
from schemas.group import GroupSchema
from keyboards import builders, inline
from services.group import GroupService
from exceptions import EntityAlreadyExists, ScheduleTimeInsertionError
from utils.states import AddGroup, AddIndiv, AddNotes, EditGroup


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
    studio_id: int = data.get('studio_id')
    start_date: WeekDays = data.get('start_date')
    group_name: str = data.get('group_name')
    group_id: int = data.get('group_id')
    group: GroupSchema = data.get('group')
    fail_count: int = data.get('fail_count', 0)

    if start_time_str == '/main':
        return await add_main(message)

    try:
        if not group_id:
            await group_service.add_schedule_to_group(
                group_id=group.id,
                start_time=datetime.strptime(start_time_str, '%H:%M').time(),
                start_date=start_date
            )
            await message.answer(
                f'Добавлено расписание день - {start_date.value}, время - '
                f'{start_time_str} для группы {group_name} '
                f'в студии {studio_name}'
            )
            await message.answer(
                f'Выбрана группа {group_name}',
                reply_markup=inline.select_group_for_studio_kb(
                    group_name=group_name, group_id=group.id,
                    studio_name=studio_name, studio_id=studio_id
                )
            )
        else:
            await group_service.add_schedule_to_group(
                group_id=group_id,
                start_time=datetime.strptime(start_time_str, '%H:%M').time(),
                start_date=start_date
            )
            await message.answer(
                f'Добавлено расписание день - {start_date.value}, время - '
                f'{start_time_str} для группы {group_name} '
                f'в студии {studio_name}'
            )
            await message.answer(
                f'Выбрана группа {group_name}',
                reply_markup=inline.select_group_for_studio_kb(
                    group_name, group_id, studio_name, studio_id
                )
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
            'занято или слишком близко к существующему расписанию.\n'
            'Попробуйте ввести другое время'
        ):
            return


@router.message(EditGroup.name)
async def edit_group_name(message: Message, state: FSMContext):
    "Check new name and edit group name"
    new_group_name = message.text
    data = await state.get_data()
    group_name = data.get('group_name')
    group_id = data.get('group_id')
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')

    if new_group_name == group_name:
        await message.answer(
            'Имя группы не может быть таким же, как и до этого. '
            'Попробуйте снова'
        )
    elif re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', new_group_name):
        await group_service.edit_group(group_id, new_group_name)
        await message.answer(
            f'Группа {group_name} успешно изменена на {new_group_name}',
            reply_markup=inline.select_group_for_studio_kb(
                group_name=new_group_name,
                group_id=group_id,
                studio_name=studio_name,
                studio_id=studio_id
            )
        )
        await state.clear()
    else:
        await message.answer(
            'Пожалуйста, введите имя группы корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(AddIndiv.start_time)
async def step3_add_indiv(message: Message, state: FSMContext):
    "Step 3. Checking the start of the indiv and creating an indiv"
    start_time_str = str(message.text)
    data = await state.get_data()
    studio_name: str = data.get('studio_name')
    studio_id: int = data.get('studio_id')
    start_date: WeekDays = data.get('start_date')
    fail_count: int = data.get('fail_count', 0)

    if start_time_str == '/main':
        return await add_main(message)

    try:
        group = await group_service.add_group(
            group_name=''.join(random.choices(string.ascii_lowercase, k=15)),
            studio_id=studio_id,
            is_individual=True
        )
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        await group_service.add_schedule_to_group(
            group_id=group.id,
            start_time=start_time,
            start_date=start_date
        )
        await message.answer(
            f'Индивидуальное занятие в студии {studio_name} '
            f'в {start_date.value} : {start_time} добавлено в рассписание'
        )
        await message.answer(
            f'Выбрана студия {studio_name}',
            reply_markup=inline.menu_studio_kb(studio_name, studio_id)
        )
        await state.clear()
    except ValueError:
        if await handle_failure(
            message, state, fail_count,
            'Время введено неверно. Пожалуйста, введите время в формате HH:MM'
        ):
            return
    except ScheduleTimeInsertionError:
        if await handle_failure(
            message, state, fail_count,
            f'Невозможно добавить расписание. Время {start_time} уже занято '
            f'или слишком близко к существующему расписанию.\n'
            'Попробуйте ввести другое время'
        ):
            return


@router.message(AddNotes.notes)
async def step2_add_group_notes(message: Message, state: FSMContext):
    "Step 2. Add notes to group"
    notes = message.text
    data = await state.get_data()
    group_name = data.get('group_name')
    group_id = data.get('group_id')
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')
    kb = inline.select_group_for_studio_kb(
        group_name, group_id, studio_name, studio_id
    )

    await group_service.edit_group(group_id=group_id, notes=notes)
    await message.answer(
        f'Заметка добавлена в группу {group_name}\n'
        f'Выбрана группа {group_name}',
        reply_markup=kb
    )
    await state.clear()
