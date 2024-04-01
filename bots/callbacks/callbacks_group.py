from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from exceptions import StudentAlreadyInGroupError
from bots.keyboards import inline, builders
from services.group import GroupService
from services.student import StudentService
from utils.states import EditGroup


router = Router()

group_service = GroupService()
student_service = StudentService()

group_list = ['pick_group', 'delete_group', 'edit_group', 'add_shedule',
              'add_student', 'list_students', 'delete_student', 'pick_groups',
              'add_student3', 'delete_indiv', 'show_schedule']


def extract_data_from_callback(
        callback_query: CallbackQuery,
        index1=3,
        index2=4,
):
    data = callback_query.data.split('_')
    return data[index1], int(data[index2])


async def group_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext | None = None
) -> None:
    """Manage callback requests related to groups."""
    group_name, group_id = extract_data_from_callback(callback)
    message = callback.message

    if action == 'pick_group':
        studio_name = callback.data.split('_')[5]
        studio_id: int = callback.data.split('_')[6]  # type: ignore
        keyboard = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
        await message.edit_text(f'Выбрана группа {group_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'delete_group':
        await group_service.delete_group(group_id)
        await message.answer(f'Группа {group_name} успешно удалена')

    elif action == 'edit_group':
        studio_name = callback.data.split('_')[5]
        await state.update_data(group_name=group_name, group_id=group_id)
        await state.set_state(EditGroup.new_group_name)
        await message.edit_text(
            f'Студия: {studio_name}\nВведите новое имя для группы {group_name}'
        )
        await message.edit_reply_markup(reply_markup=None)

    elif action == 'add_shedule':
        studio_id: int = int(callback.data.split('_')[5])
        studio_name: str = callback.data.split('_')[6]
        await state.update_data(
            group_name=group_name,
            group_id=group_id,
            studio_id=studio_id,
            studio_name=studio_name
        )
        await message.edit_text(
            f'Выберите день занятия для группы {group_name}'
        )
        await message.edit_reply_markup(
            reply_markup=await builders.process_select_weekdays(
                action='weekday_group'  # type: ignore
            )
        )

    elif action == 'add_student':
        keyboard = await builders.show_list_students_menu(
            action='add_student2'
        )
        await state.update_data(group_name=group_name, group_id=group_id)
        await message.edit_text(
            f'Выберите ученика для добавления его в группу {group_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'list_students':
        keyboard = await builders.show_list_students_from_group_menu(
            'pick_student', group_id
        )
        keyboard2 = await builders.show_list_studios_menu('list_group')
        students = await student_service.get_students_from_group(group_id)

        if not students:
            await message.edit_text(
                f'Учеников нет в группе {group_name}. Выберите другую группу'
            )
            await message.edit_reply_markup(reply_markup=keyboard2)
            return

        await message.edit_text(f'Список учеников для группы {group_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'delete_student':
        students = await student_service.get_students_from_group(group_id)
        if students:
            keyboard = await builders.show_list_students_from_group_menu(
                'delete_students', group_id
            )
            await state.update_data(group_name=group_name, group_id=group_id)
            await message.edit_text(
                f'Выберите ученика для удаления его из группы {group_name}'
            )
            await message.edit_reply_markup(reply_markup=keyboard)
        else:
            await message.edit_text(
                f'В группе - {group_name} нет учеников. Выберите другую группу'
            )
            await message.edit_reply_markup(reply_markup=None)

    elif action == 'pick_groups':
        #  student_name: str = callback.data.split('_')[5]
        #  student_id: int = int(callback.data.split('_')[6])
        keyboard = inline.select_student_for_group_kb(group_name, group_id)
        await message.edit_text('Выбери сцука')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'add_student3':
        data = await state.get_data()
        studio_name = data.get('studio_name', '1')
        studio_id: int = data.get('studio_id', 1)
        student_name = data.get('student_name')
        student_id: int = data.get('student_id', 1)
        keyboard = await builders.show_list_groups_menu(
            action='add_student3',
            studio_name=studio_name,
            studio_id=studio_id
        )

        try:
            await student_service.add_student_to_group(
                student_id=student_id,
                group_id=group_id,
                is_individual=False
            )
            await message.edit_text(
                f'Ученик {student_name} добавлен в группу {group_name}'
            )
            await state.clear()

        except StudentAlreadyInGroupError:
            await message.answer(
                f'Ученик {student_name} уже находится в {group_name}. '
                f'Выберите другую группу:',
                reply_markup=keyboard
            )

    elif action == 'delete_indiv':
        await group_service.delete_group(group_id)
        await message.answer(f'Индив {group_name} успешно удалена')
        await message.edit_reply_markup(reply_markup=None)

    elif action == 'show_schedule':
        schedules = await group_service.get_date_time_group(group_id=group_id)
        if schedules:
            keyboard = await builders.show_list_schedules_for_group(
                'call_group_schedule', schedules
            )
            await message.edit_text(
                f'Список всех занятий в группе {group_name}'
            )
            await message.edit_reply_markup(
                reply_markup=keyboard  # type: ignore
            )
        else:
            await message.edit_text('В группе нет занятий')
            await message.edit_reply_markup(reply_markup=None)
