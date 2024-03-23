from aiogram.types import CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from utils.states import EditStudent
from bots.callbacks.callbacks_studio import extract_data_from_callback
from bots.keyboards import builders, inline
from services.student import StudentService


router = Router()

student_service = StudentService()


async def student_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext = None  # type: ignore
) -> None:
    student_name, student_id = extract_data_from_callback(callback)
    message = callback.message

    if action == 'pick_student':
        keyboard = inline.select_students_kb(student_name, student_id)
        await message.edit_text(f'Выбран ученик - {student_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'add_student2':
        data = await state.get_data()
        group_name: str = data.get('group_name', 'Проблема')
        group_id: int = data.get('group_id', -1)
        await student_service.add_student_to_group(student_id, group_id)
        await message.edit_text(
            f'Ученик {student_name} успешно добавлен в группу {group_name}'
        )
        await message.edit_reply_markup(reply_markup=None)
        await state.clear()

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
        keyboard = await builders.process_show_group_for_student(
            student_id, student_name
        )
        await message.edit_text(
            f'Список групп, в которых учится - {student_name}'
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


# Выбор ученика для дальнешего взаимодействия
@router.callback_query(F.data.startswith('pick_student_'))
async def select_students(callback: CallbackQuery) -> None:
    await student_callback(callback, 'pick_student')


@router.callback_query(F.data.startswith('add_student2_'))
async def select_student_for_group(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await student_callback(callback, 'add_student2', state)


@router.callback_query(F.data.startswith('delete_students_'))
async def call_delete_students_from_group(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await student_callback(callback, 'delete_students', state)


# Удаление ученика из БД
@router.callback_query(F.data.startswith('fulldelete_student_'))
async def call_delete_student(callback: CallbackQuery) -> None:
    await student_callback(callback, 'fulldelete_student')


@router.callback_query(F.data.startswith('show_group_'))
async def call_show_group(callback: CallbackQuery) -> None:
    await student_callback(callback, 'show_group')


# Редактирование имени ученика
@router.callback_query(F.data.startswith('edit_student_'))
async def call_edit_student_name(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await student_callback(callback, 'edit_student', state)


@router.callback_query(F.data.startswith('select_student_'))
async def call_show_group_to_add_student(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await student_callback(callback, 'select_student', state)
