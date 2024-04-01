import random
import string
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bots.keyboards import builders, inline
from services.group import GroupService
from services.studio import StudioService
from utils.states import EditStudio, Group
from bots.callbacks.callbacks_group import group_callback, group_list
from bots.callbacks.callbacks_student import student_callback, student_list
from bots.callbacks.callbacks_schedule import schedule_callback, schedule_list


router = Router()

studio_service = StudioService()
group_service = GroupService()


@router.callback_query(F.data.startswith('call_'))
async def callback_studio_request(
    callback: CallbackQuery,
    state: FSMContext | None,
) -> None:
    action = '_'.join(callback.data.split('_')[1:3])
    if action in group_list:
        await group_callback(callback, action, state)
    elif action in student_list:
        await student_callback(callback, action, state)
    elif action in schedule_list:
        await schedule_callback(callback, action, state)
    else:
        await studio_callback(callback, action, state)


def extract_data_from_callback(
        callback_query: CallbackQuery,
        index1=3,
        index2=4,
):
    data = callback_query.data.split('_')
    return data[index1], int(data[index2])


async def studio_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext | None = None,
) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)
    message = callback.message

    if action == 'pick_studio':
        keyboard = inline.create_studio_kb(
            studio_name=studio_name,
            studio_id=studio_id,
        )
        await message.edit_text(f'Выбрана студия {studio_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'delete_studio':
        await studio_service.delete_studio(studio_id)
        await message.answer(f'Студия {studio_name} успешно удалена')

    elif action == 'edit_studio':
        await state.update_data(studio_id=studio_id, studio_name=studio_name)
        await state.set_state(EditStudio.new_studio_name)
        await message.edit_text(f'Введите новое имя для студии {studio_name}')

    elif action == 'select_studio':
        await state.update_data(studio_id=studio_id, studio_name=studio_name)
        await message.edit_text(
            f'Введите название для новой группы в студии {studio_name}'
        )
        await state.set_state(Group.group_name)

    elif action == 'list_group':
        groups = await group_service.get_groups(studio_id)
        keyboard = await builders.show_list_studios_menu(action='list_group')
        if not groups:
            await message.edit_text(
                f'Увы, в студии {studio_name} пока нет групп. '
                'Пожалуйста, выберите другую студию.'
            )
            await message.edit_reply_markup(reply_markup=keyboard)
            return
        await message.edit_text(f'Список групп для студии {studio_name}')
        await message.edit_reply_markup(
            reply_markup=await builders.show_list_groups_menu(
                action='pick_group',
                studio_name=studio_name,
                studio_id=studio_id
            ))

    elif action == 'delete_groups':
        await message.edit_text(
            f'Выберите группу для удаления в студии {studio_name}')
        await message.edit_reply_markup(
            reply_markup=await builders.show_list_groups_menu(
                'delete_group', studio_name, studio_id))

    elif action == 'list_studios':
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

    elif action == 'select_studios':
        keyboard = await builders.show_list_indiv_menu(
            action='delete_indiv',
            studio_name=studio_name,
            studio_id=studio_id
        )
        await message.edit_text(
            f'Выбери индив, который необходимо удалить из студии {studio_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)
