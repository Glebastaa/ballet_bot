from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from exceptions import StudentAlreadyInGroupError
from keyboards import inline, builders
from services.student import StudentService
from services.group import GroupService
from utils.states import EditStudent


router = Router()
student_service = StudentService()
group_service = GroupService()


def extract_data_from_callback(callback: CallbackQuery, index1=1, index2=2):
    data = callback.data.split('_')
    return data[index1], int(data[index2])


@router.callback_query(F.data.startswith('listStudents'))
async def list_students(callback: CallbackQuery):
    "Show the list of studios from the show menu"
    student_name, student_id = extract_data_from_callback(callback)
    kb = inline.select_students_kb(student_name, student_id)

    await callback.message.edit_text(f'Выбран ученик - {student_name}')
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('editStudent'))
async def edit_student(callback: CallbackQuery, state: FSMContext):
    student_name, student_id = extract_data_from_callback(callback)

    await state.update_data(student_name=student_name, student_id=student_id)
    await state.set_state(EditStudent.name)
    await callback.message.edit_text(
        f'Введите новое имя для ученика {student_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('addStudentToGroup'))
async def step1_add_student_to_group(
    callback: CallbackQuery,
    state: FSMContext
):
    "Check and add student to group"
    student_name, student_id = extract_data_from_callback(callback)
    data = await state.get_data()
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')
    group_name = data.get('group_name')
    group_id = data.get('group_id')
    kb = inline.select_group_for_studio_kb(
        group_name, group_id, studio_name, studio_id
    )

    try:
        await student_service.add_student_to_group(student_id, group_id)
        await callback.message.edit_text(
            f'Ученик {student_name} добавлен в группу {group_name}\n'
            f'Выбрана группа {group_name}'
        )
        await callback.message.edit_reply_markup(
            reply_markup=kb
        )
    except StudentAlreadyInGroupError:
        await callback.message.edit_text(
            f'Ученик {student_name} уже добавлен в группу {group_name}\n'
            f'Выбрана группа {group_name}'
        )
        await callback.message.edit_reply_markup(
            reply_markup=kb
        )
    await state.clear()


@router.callback_query(F.data.startswith('deleteStudentToGroup2'))
async def step2_delete_student_to_group(
    callback: CallbackQuery, state: FSMContext
):
    "Step 2. Delete student in the group"
    student_name, student_id = extract_data_from_callback(callback)
    data = await state.get_data()
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')
    group_name = data.get('group_name')
    group_id = data.get('group_id')
    kb = inline.select_group_for_studio_kb(
        group_name, group_id, studio_name, studio_id
    )

    await student_service.delete_student_from_group(student_id, group_id)
    await callback.message.edit_text(
        f'Ученик {student_name} удален\nВыбрана группа {group_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)
    await state.clear()
