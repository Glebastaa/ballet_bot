from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import inline, builders
from services.group import GroupService
from services.student import StudentService
from utils.states import AddNotes, EditGroup

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


@router.callback_query(F.data.startswith('addScheduleGroup'))
async def step1_add_group_schedule(
    callback: CallbackQuery, state: FSMContext
):
    "Step 1. Add schedule to group"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    kb = await builders.select_weekdays('weekdayGroup')

    await state.update_data(
        group_name=group_name, group_id=group_id,
        studio_name=studio_name, studio_id=studio_id
    )
    await callback.message.edit_text(
                'Выберите день, когда будет проходить '
                f'занятии в группе {group_name}',
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('showScheduleGroup'))
async def show_group_schedule(callback: CallbackQuery):
    "Show group schedule"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    schedules = await group_service.get_date_time_group(group_id)
    if schedules:
        kb = inline.back_to_group_menu(
            group_name, group_id, studio_name, studio_id
        )
        list_schedules = '\n'.join([
            f'{schedule.start_date.value} : {schedule.start_time}'
            for schedule in schedules
        ])

        await callback.message.edit_text(
            f'Список занятий:\n{list_schedules}'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
    else:
        kb = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
        await callback.message.edit_text(
            f'В этой группе еще нету занятий\nВыбрана группа {group_name}'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('deleteScheduleGroup'))
async def step1_delete_group_schedule(
    callback: CallbackQuery, state: FSMContext
):
    "delete schedule group"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    schedules = await group_service.get_date_time_group(group_id)

    await state.update_data(
        group_name=group_name, group_id=group_id,
        studio_name=studio_name, studio_id=studio_id
    )
    if schedules:
        kb = await builders.show_list_schedules_to_group(
            'deleteScheduleGroup2', schedules
        )
        await callback.message.edit_text(
            'Выберите занятие, которое хотите удалить'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
    else:
        kb = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
        await callback.message.edit_text(
            f'В этой группе еще нету занятий\nВыбрана группа {group_name}'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('addNotesToGroup'))
async def step1_add_group_note(
    callback: CallbackQuery, state: FSMContext
):
    "TODO"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]

    await state.update_data(
        group_name=group_name, group_id=group_id,
        studio_name=studio_name, studio_id=studio_id
    )
    await state.set_state(AddNotes.notes)
    await callback.message.edit_text(
        f'Напишите заметку для группы {group_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('showNotesToGroup'))
async def show_group_note(callback: CallbackQuery):
    "TODO"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    note = await group_service.get_notes(group_id)
    if note:
        kb = inline.back_to_group_menu(
            group_name, group_id, studio_name, studio_id
        )
        await callback.message.edit_text(note)
        await callback.message.edit_reply_markup(reply_markup=kb)
    else:
        kb = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
        await callback.message.edit_text(
            f'В группе {group_name} заметки не найдено'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('deleteNotesGroup'))
async def delete_group_note(callback: CallbackQuery):
    "TODO"
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split('_')[3]
    studio_id: int = callback.data.split('_')[4]
    note = await group_service.get_notes(group_id)
    kb = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
    if note:
        await group_service.delete_notes(group_id)
        await callback.message.edit_text(
            f'Заметка в группе {group_name} удалена'
        )
    else:
        await callback.message.edit_text(
            f'В группе {group_name} заметки не найдено'
        )
    await callback.message.edit_reply_markup(reply_markup=kb)
