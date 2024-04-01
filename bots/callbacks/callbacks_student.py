from aiogram.types import CallbackQuery
from aiogram import Router
from aiogram.fsm.context import FSMContext

from exceptions import StudentAlreadyInGroupError
from services.group import GroupService
from utils.states import EditStudent
from bots.keyboards import builders, inline
from services.student import StudentService


router = Router()

student_service = StudentService()
group_service = GroupService()

student_list = ['pick_student', 'add_student2', 'delete_students',
                'fulldelete_student', 'show_group', 'edit_student',
                'select_student']


def extract_data_from_callback(
        callback_query: CallbackQuery,
        index1=3,
        index2=4,
):
    data = callback_query.data.split('_')
    return data[index1], int(data[index2])


async def student_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext | None = None
) -> None:
    student_name, student_id = extract_data_from_callback(callback)
    message = callback.message

    if action == 'pick_student':
        keyboard = inline.select_students_kb(student_name, student_id)
        await message.edit_text(f'Выбран ученик - {student_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'add_student2':
        try:
            data = await state.get_data()
            group_name: str = data.get('group_name', 'Проблема')
            group_id: int = data.get('group_id', -1)
            await student_service.add_student_to_group(student_id, group_id)
            await message.edit_text(
                f'Ученик {student_name} успешно добавлен в группу {group_name}'
            )
            await state.clear()
        except StudentAlreadyInGroupError:
            keyboard = await builders.show_list_students_menu(
                action='add_student2'
            )
            await message.edit_text(
                f'{student_name} уже состоит в группе {group_name}. '
                'Выберите другого ученика для добавления в группу'
            )
            await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'delete_students':
        data = await state.get_data()
        group_name: str = data.get('group_name', 'Проблема')
        group_id: int = data.get('group_id', -1)
        await student_service.delete_student_from_group(student_id, group_id)
        await message.edit_text(
            f'Ученик {student_name} успешно удален из группы {group_name}'
        )

    elif action == 'fulldelete_student':
        await student_service.delete_student(student_id)
        await message.answer(f'Ученик {student_name} успешно удален')

    elif action == 'show_group':
        groups = await group_service.get_groups_from_student(student_id)
        if groups:
            keyboard = await builders.process_show_group_for_student(
                student_id, student_name
            )
            await message.edit_text(
                f'Список групп, в которых учится - {student_name}'
            )
            await message.edit_reply_markup(reply_markup=keyboard)
        else:
            keyboard = await builders.show_list_students_menu(
                action='pick_student'
            )
            await message.edit_text(
                f'Ученик {student_name} не добавлен не в 1 группу'
            )
            await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'edit_student':
        await state.update_data(
            student_name=student_name,
            student_id=student_id
        )
        await state.set_state(EditStudent.new_student_name)
        await message.edit_text(
            f'Введите новое имя ученика {student_name}'
        )
        await message.edit_reply_markup(reply_markup=None)

    elif action == 'select_student':
        await state.update_data(
            student_name=student_name,
            student_id=student_id
        )
        keyboard = await builders.show_list_studios_menu('show_studios')
        await message.edit_text(
            f'Выберите студию, в которой будет заниматся ученик {student_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)
