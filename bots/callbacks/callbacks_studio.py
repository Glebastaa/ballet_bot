import random
import string
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bots.keyboards import builders, inline
from services.group import GroupService
from services.studio import StudioService
from utils.states import EditStudio


router = Router()

studio_service = StudioService()
group_service = GroupService()


def extract_data_from_callback(
        callback_query: CallbackQuery,
        index1=2,
        index2=3,
):
    data = callback_query.data.split('_')
    return data[index1], int(data[index2])


async def studio_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext = None,  # type: ignore
) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)
    message = callback.message

    if action == 'pick_studio':
        keyboard = inline.create_studio_kb(
            studio_name=studio_name,
            studio_id=studio_id
        )
        await message.edit_text(f'Выбрана студия {studio_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'delete_studio':
        await studio_service.delete_studio(studio_id)
        await message.answer(f'Студия {studio_name} успешно удалена')

    elif action == 'edit_name_studio':
        await state.update_data(studio_id=studio_id, studio_name=studio_name)
        await state.set_state(EditStudio.new_studio_name)
        await message.edit_text(f'Введите новое имя для студии {studio_name}')

    elif action == 'select_studio_from_create_indiv':
        data = await state.get_data()
        group_name: str = data.get('group_name', 'Пуп')
        await group_service.add_group(group_name, studio_id)
        await message.edit_text(
            f'Группа {group_name} успешно создана и '
            f'добавлена в студию {studio_name}'
        )

    elif action == 'list_groups_from_studio':
        groups = await group_service.get_groups(studio_id)
        keyboard = await builders.show_list_studios_menu(action='list_group')
        if not groups:
            await message.edit_text(
                f'Увы, в студии {studio_name} пока нет групп. '
                'Пожалуйста, выберите другую студию.'
            )
            await message.edit_reply_markup(
                'Выберите студию',
                reply_markup=keyboard)
            return
        await message.edit_text(f'Список групп для студии {studio_name}')
        await message.edit_reply_markup(
            reply_markup=await builders.show_list_groups_menu(
                'pick_group', studio_name, studio_id))

    elif action == 'select_group_from_delete':
        await message.edit_text(
            f'Выберите группу для удаления в студии {studio_name}')
        await message.edit_reply_markup(
            reply_markup=await builders.show_list_groups_menu(
                'delete_group', studio_name, studio_id))

    elif action == 'list_studios_from_group':
        keyboard = await builders.show_list_groups_menu(
            'edit_group', studio_name, studio_id
        )
        await message.edit_text(
            f'Список групп для студии {studio_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'add_indiv':
        keyboard = await builders.process_select_weekdays(
            action='weekday_indiv'
        )
        group_name = ''.join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )

        indiv = await group_service.add_group(
            group_name, studio_id, is_individual=True
        )
        await state.update_data(
            group_name=group_name,
            studio_id=studio_id,
            studio_name=studio_name,
            indiv=indiv
        )
        await message.edit_text(
            f'Выберите, в какой день будет проходить '
            f'занятие в студии {studio_name}')
        await message.edit_reply_markup(reply_markup=keyboard)  # type: ignore

    elif action == 'show_studios':
        keyboard = await builders.show_list_groups_menu(
            'add_student3', studio_name, studio_id
        )
        data = await state.get_data()
        student_name: str = data.get('student_name', '1')
        await state.update_data(studio_name=studio_name, studio_id=studio_id)
        await message.edit_text(
            f'Выберите группу, в которой будет заниматся {student_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'select_studio_for_delete_indiv':
        keyboard = await builders.show_list_indiv_menu(
            action='delete_indiv',
            studio_name=studio_name,
            studio_id=studio_id
        )
        await message.edit_text(
            f'Выбери индив, который необходимо удалить из студии {studio_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data.startswith('pick_studio_'))
async def call_select_studio(
    callback: CallbackQuery
):
    await studio_callback(callback, 'pick_studio')


@router.callback_query(F.data.startswith('delete_studio_'))
async def call_delete_studio(
    callback: CallbackQuery
) -> None:
    await studio_callback(callback, 'delete_studio')


@router.callback_query(F.data.startswith('edit_studio_'))
async def call_edit_studio(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await studio_callback(callback, 'edit_name_studio', state)


@router.callback_query(F.data.startswith('select_studio_'))
async def select_studio_for_group(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await studio_callback(callback, 'select_studio_from_create_indiv', state)


@router.callback_query(F.data.startswith('list_group_'))
async def call_list_groups(
    callback: CallbackQuery
) -> None:
    await studio_callback(callback, 'list_groups_from_studio')


@router.callback_query(F.data.startswith('delete_groups_'))
async def call_select_group_from_delete(
    callback: CallbackQuery
) -> None:
    await studio_callback(callback, 'select_group_from_delete')


# Список групп для выбранной студии
@router.callback_query(F.data.startswith('list_studios_'))
async def call_list_studios(
    callback: CallbackQuery
) -> None:
    await studio_callback(callback, 'list_studios_from_group')


# Выбор студии для добавления индива с переходом в выбор start_time
@router.callback_query(F.data.startswith('add_indiv_'))
async def call_add_indiv_to_studio(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await studio_callback(callback, 'add_indiv', state)


@router.callback_query(F.data.startswith('show_studios_'))
async def call_select_studio_for_student(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await studio_callback(callback, 'show_studios', state)


@router.callback_query(F.data.startswith('select_studios_'))
async def call_select_studio_for_delete_indiv(
    callback: CallbackQuery,
) -> None:
    await studio_callback(callback, 'select_studio_for_delete_indiv')
