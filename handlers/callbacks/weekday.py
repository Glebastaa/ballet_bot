from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models import WeekDays
from utils.states import AddGroup, AddIndiv


router = Router()


@router.callback_query(F.data.startswith('weekdayGroup'))
async def step3_add_group(callback: CallbackQuery, state: FSMContext):
    "Step 3. Add weekday to state for add group"
    start_date = WeekDays(callback.data.split('_')[1])

    await state.update_data(start_date=start_date)
    await state.set_state(AddGroup.start_time)
    await callback.message.edit_text(
        f'Введите время начала занятия в {start_date.value}'
    )


@router.callback_query(F.data.startswith('weekdayIndiv'))
async def step2_add_indiv(callback: CallbackQuery, state: FSMContext):
    "Step 2. Saving the class day in state"
    start_date = WeekDays(callback.data.split('_')[1])

    await state.update_data(start_date=start_date)
    await state.set_state(AddIndiv.start_time)
    await callback.message.edit_text(
        f'Введите время начала занятия в {start_date.value}'
    )
