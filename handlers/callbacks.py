from aiogram.types import CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from keyboards import inline, builders
from services.group import GroupService
from services.studio import StudioService
from utils.states import EditStudio

router = Router()


def extract_data_from_callback(callback: CallbackQuery, index1=1, index2=2):
    data = callback.data.split('_')
    return data[index1], int(data[index2])


@router.callback_query(F.data.startswith('listStudio_'))
async def list_studio(callback: CallbackQuery):
    "Show the list of studios from the main menu"
    studio_name, studio_id = extract_data_from_callback(callback)
    kb = inline.create_studio_kb(studio_name, studio_id)

    await callback.message.edit_text(f'Выбрана студия {studio_name}')
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('editStudio_'))
async def edit_studio(callback: CallbackQuery, state: FSMContext):
    "Editing the studio name"
    studio_name, studio_id = extract_data_from_callback(callback)

    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    await state.set_state(EditStudio.name_update)
    await callback.message.edit_text(
        f'Введите новое имя для студии {studio_name}'
    )


@router.callback_query(F.data.startswith('deleteStudio_'))
async def delete_studio(callback: CallbackQuery):
    "Delete studio"
    studio_name, studio_id = extract_data_from_callback(callback)

    await StudioService().delete_studio(studio_id)
    await callback.message.answer(f'Студия {studio_name} успешно удалена!')


@router.callback_query(F.data.startswith('listGroupsByStudio_'))
async def list_groups_by_studio(callback: CallbackQuery):
    "Show the list groups from the pick studio"
    studio_name, studio_id = extract_data_from_callback(callback)
    groups = await GroupService().get_groups(studio_id)
    if not groups:
        await callback.message.edit_text(
            f'Увы, в студии {studio_name} пока нет групп. '
            'Пожалуйста, выберите другую студию.'
        )
        await callback.message.edit_reply_markup(
            reply_markup=await builders.show_list_studios_menu(
                'listGroupsByStudio'
            )
        )
        return

    await callback.message.edit_text(f'Список групп для студии {studio_name}')
    await callback.message.edit_reply_markup(
        reply_markup=await builders.show_list_groups_for_studio(
            studio_name, studio_id
        ))


@router.callback_query(F.data.startswith('selectGroupByStudio_'))
async def show_group_menu(callback: CallbackQuery):
    "Group menu"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    kb = inline.select_group_for_studio_kb(group_name, group_id, studio_name)

    await callback.message.edit_text(f'Выбрана группа {group_name}')
    await callback.message.edit_reply_markup(reply_markup=kb)
