from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import inline

router = Router()


def extract_data_from_callback(callback: CallbackQuery, index1=1, index2=2):
    data = callback.data.split('_')
    return data[index1], int(data[index2])


@router.callback_query(F.data.startswith('selectGroupByStudio'))
async def show_group_menu(callback: CallbackQuery):
    "Group menu"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    kb = inline.select_group_for_studio_kb(group_name, group_id, studio_name)

    await callback.message.edit_text(f'Выбрана группа {group_name}')
    await callback.message.edit_reply_markup(reply_markup=kb)
