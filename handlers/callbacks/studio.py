from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import inline, builders
from services.studio import StudioService
from services.group import GroupService
from utils.states import AddGroup, AddIndiv, EditStudio


router = Router()
studio_service = StudioService()
group_service = GroupService()


def extract_data_from_callback(callback: CallbackQuery, index1=1, index2=2):
    data = callback.data.split('_')
    return data[index1], int(data[index2])


@router.callback_query(F.data.startswith('selectStudio'))
async def list_studios(callback: CallbackQuery):
    "Show the list of studios from the main menu"
    studio_name, studio_id = extract_data_from_callback(callback)
    kb = inline.menu_studio_kb(studio_name, studio_id)

    await callback.message.edit_text(f'Выбрана студия {studio_name}')
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('editStudio'))
async def edit_studio(callback: CallbackQuery, state: FSMContext):
    "Editing the studio name"
    studio_name, studio_id = extract_data_from_callback(callback)

    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    await state.set_state(EditStudio.name_update)
    await callback.message.edit_text(
        f'Введите новое имя для студии {studio_name}'
    )


@router.callback_query(F.data.startswith('deleteStudio'))
async def delete_studio(callback: CallbackQuery):
    "Delete studio"
    studio_name, studio_id = extract_data_from_callback(callback)

    await studio_service.delete_studio(studio_id)
    await callback.message.answer(f'Студия {studio_name} успешно удалена!')


@router.callback_query(F.data.startswith('listGroupsByStudio'))
async def list_groups_by_studio(callback: CallbackQuery, state: FSMContext):
    "Show the list groups from the pick studio"
    studio_name, studio_id = extract_data_from_callback(callback)
    groups = await group_service.get_groups(studio_id)
    if not groups:
        await state.update_data(studio_name=studio_name, studio_id=studio_id)
        await state.set_state(AddGroup.name)
        await callback.message.edit_text(
            f'Увы, в студии {studio_name} пока нет групп. '
            'Давайте ее создадим. Введите имя для группы'
        )
        await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.edit_text(f'Список групп для студии {studio_name}')
    await callback.message.edit_reply_markup(
        reply_markup=await builders.show_list_groups_for_studio(
            'selectGroupByStudio', studio_name, studio_id
        ))


@router.callback_query(F.data.startswith('addGroupBySelectStudio'))
async def step1_add_group(callback: CallbackQuery, state: FSMContext):
    "Step 1. Select studio by add group"
    studio_name, studio_id = extract_data_from_callback(callback)

    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    await state.set_state(AddGroup.name)
    await callback.message.edit_text(
        f'Введите название для новой группы в студии {studio_name}'
    )


@router.callback_query(F.data.startswith('editGroupBySelectStudio'))
async def edit_group_name(callback: CallbackQuery):
    "Select group to change name"
    studio_name, studio_id = extract_data_from_callback(callback)
    kb = await builders.show_list_groups_for_studio(
        'editGroupName', studio_name, studio_id
    )
    await callback.message.edit_text(
        f'Выберите группу в студии {studio_name} для смены имени:'
    )
    await callback.message.edit_reply_markup(
        reply_markup=kb
    )


@router.callback_query(F.data.startswith('selectStudioByAddStudent'))
async def step2_add_student_to_group(
    callback: CallbackQuery,
    state: FSMContext
):
    "Step 2. Save studio to state and transition to select group"
    studio_name, studio_id = extract_data_from_callback(callback)
    kb = await builders.show_list_groups_for_studio(
        'selectGroupByAddStudent', studio_name, studio_id
    )
    data = await state.get_data()
    student_name = data.get('student_name')

    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    await callback.message.edit_text(
        f'Выбериту группу в студии {studio_name}, в '
        f'которой будет заниматся {student_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('addIndiv'))
async def step1_add_indiv(callback: CallbackQuery, state: FSMContext):
    "TODO"
    studio_name, studio_id = extract_data_from_callback(callback)
    kb = await builders.select_weekdays('weekdayIndiv')

    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    await callback.message.edit_text(
        f'Выберите день, когда будет проходить занятие в студии {studio_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('listIndiv'))
async def show_studio_indiv_lesson(callback: CallbackQuery, state: FSMContext):
    "TODO"
    studio_name, studio_id = extract_data_from_callback(callback)
    indivs = await group_service.get_date_time_indivs_by_studio(studio_id)
    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    if indivs:
        kb = await builders.show_list_schedules_to_group(
            'menuIndiv', schedules=indivs
        )
        await callback.message.edit_text(
            f'Список индивов в студии {studio_name}:'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
    else:
        kb = await builders.select_weekdays('weekdayIndiv')
        await state.update_data(studio_name=studio_name, studio_id=studio_id)
        await callback.message.edit_text(
            f'Увы, в студии {studio_name} еще нет индивидуальных занятий\n'
            'Давайте ее создадим. Выберите день, когда будет проходить занятие'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
