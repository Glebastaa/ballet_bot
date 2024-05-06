from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import inline, builders
from services.group import GroupService
from services.student import StudentService
from utils.states import AddStudent, EditGroup

router = Router()
student_service = StudentService()
group_service = GroupService()


def extract_data_from_callback(callback: CallbackQuery, index1=1, index2=2):
    data = callback.data.split('_')
    return data[index1], int(data[index2])


@router.callback_query(F.data.startswith('selectGroupByStudio'))
async def show_group_menu(callback: CallbackQuery):
    "Group menu"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id = callback.data.split('_')[4]
    kb = inline.select_group_for_studio_kb(
        group_name, group_id, studio_name, studio_id
    )

    await callback.message.edit_text(f'Выбрана группа {group_name}')
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('editGroup'))
async def edit_group_name(callback: CallbackQuery, state: FSMContext):
    "Requesting a new group name"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id = callback.data.split('_')[4]
    await state.update_data(
        group_name=group_name,
        group_id=group_id,
        studio_name=studio_name,
        studio_id=studio_id
    )
    await state.set_state(EditGroup.name)
    await callback.message.edit_text(
        f'Студия: {studio_name}\nВведите новое имя для группы {group_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('deleteGroup'))
async def delete_group(callback: CallbackQuery):
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id = callback.data.split('_')[4]
    kb = inline.menu_studio_kb(studio_name, studio_id)

    await group_service.delete_group(group_id)
    await callback.message.edit_text(
        f'Группа {group_name} удалена\nВыбрана студия {studio_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('deleteStudentFromGroup'))
async def delete_student_by_group(callback: CallbackQuery):
    "Removing a student from a group"
    group_name, group_id = extract_data_from_callback(callback)
    student_name = callback.data.split('_')[3]
    student_id: int = callback.data.split('_')[4]

    await student_service.delete_student_from_group(student_id, group_id)
    await callback.message.edit_text(
        f'Ученик {student_name} удален из группы {group_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('selectStudentToGroup'))
async def step1_add_student_to_group(
    callback: CallbackQuery,
    state: FSMContext
):
    "Step 1. Add student to group"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    kb = await builders.show_all_students('addStudentToGroup')
    students = await student_service.get_all_students()

    if students:
        await state.update_data(
            group_name=group_name, group_id=group_id,
            studio_name=studio_name, studio_id=studio_id
        )
        await callback.message.edit_text(
            f'Выберите ученика для добавления в группу {group_name}'
        )
        await callback.message.edit_reply_markup(
            reply_markup=kb
        )
    else:
        await callback.message.answer('Мимо')


@router.callback_query(F.data.startswith('showStudentToGroup'))
async def show_list_students_to_group(callback: CallbackQuery):
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    students = await student_service.get_students_from_group(group_id)

    if students:
        kb = inline.back_to_group_menu(
            group_name, group_id, studio_name, studio_id
        )
        list_students = '\n'.join([str(student.name) for student in students])
        await callback.message.edit_text(
            f'Список учеников:\n{list_students}'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
    else:
        kb = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
        await callback.message.edit_text('В этой группе еще нет студентов')
        await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('deleteStudentToGroup'))
async def step1_delete_student_to_group(
    callback: CallbackQuery, state: FSMContext
):
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    await state.update_data(
        group_name=group_name, group_id=group_id,
        studio_name=studio_name, studio_id=studio_id
    )
    students = await student_service.get_students_from_group(group_id)
    if students:
        kb = await builders.show_students_to_group(
            'deleteStudentToGroup2', group_id
        )
        await callback.message.edit_text(
            'Выберите ученика для удаления из группы'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
    else:
        kb = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
        await callback.message.edit_text(
            f'В этой группе еще нет студентов\nВыбрана группа {group_name}'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
