from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.states import AddGroup
from database.models import WeekDays


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
