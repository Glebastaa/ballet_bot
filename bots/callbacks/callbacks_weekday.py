from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.states import AddIndiv, Group
from database.models import WeekDays
from services.group import GroupService


router = Router()
group_service = GroupService()


async def weekday_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext = None  # type: ignore
) -> None:
    start_date = WeekDays(callback.data.split('_')[2])
    message = callback.message

    if action == 'weekday_indiv':
        await state.update_data(start_date=start_date)
        await state.set_state(AddIndiv.start_time)
        await message.edit_text(
            'Введите время начала индивидуального занятия '
            f'в {start_date.value}'
        )
        await message.edit_reply_markup(reply_markup=None)

    elif action == 'weekday_group':
        await state.update_data(start_date=start_date)
        await state.set_state(Group.start_time)
        await message.edit_text(
            f'Введите время начала занятия в {start_date.value}'
        )


@router.callback_query(F.data.startswith('weekday_indiv_'))
async def select_weekday_for_indiv(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await weekday_callback(callback, 'weekday_indiv', state)


@router.callback_query(F.data.startswith('weekday_group_'))
async def call_add_weekday_from_group(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await weekday_callback(callback, 'weekday_group', state)
