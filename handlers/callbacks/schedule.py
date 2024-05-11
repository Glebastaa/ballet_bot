from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.group import GroupService
from services.student import StudentService
from keyboards import inline, builders


router = Router()
group_service = GroupService()
student_service = StudentService()


@router.callback_query(F.data.startswith('deleteScheduleGroup2'))
async def step2_delete_group_schedule(
    callback: CallbackQuery,
    state: FSMContext
):
    start_date = callback.data.split('_')[1]
    start_time = callback.data.split('_')[2]
    schedule_id = int(callback.data.split('_')[3])
    data = await state.get_data()
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')
    group_name = data.get('group_name')
    group_id = data.get('group_id')
    kb = inline.select_group_for_studio_kb(
        group_name, group_id, studio_name, studio_id
    )

    await group_service.delete_schedule(schedule_id)
    await callback.message.edit_text(
        f'Занятие в {start_date} : {start_time} удалено\n'
        f'Выбрана группа {group_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)
    await state.clear()


@router.callback_query(F.data.startswith('menuIndiv'))
async def menu_indiv(
    callback: CallbackQuery,
    state: FSMContext
):
    start_date = callback.data.split('_')[1]
    start_time = callback.data.split('_')[2]
    schedule_id = int(callback.data.split('_')[3])
    group_id = int(callback.data.split('_')[4])
    data = await state.get_data()
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')
    kb = inline.select_schedule_to_studio_kb(
        start_date, start_time, schedule_id, studio_name, studio_id, group_id
    )

    await callback.message.edit_text(
        f'Выбрано индивидаульное занятие в {start_date} : {start_time}\n'
        'Выберите действие:'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('deleteIndiv'))
async def delete_indiv(callback: CallbackQuery):
    start_date = callback.data.split('_')[1]
    start_time = callback.data.split('_')[2]
    studio_name = callback.data.split('_')[4]
    studio_id = callback.data.split('_')[5]
    group_id = int(callback.data.split('_')[6])
    kb = inline.menu_studio_kb(studio_name, studio_id)

    await group_service.delete_group(group_id)
    await callback.message.edit_text(
        f'Индивидуальное занятие в {start_date} : {start_time} '
        f'удалено из студии {studio_name}\n'
        f'Выбрана студия {studio_name}'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('selectStudentToIndiv'))
async def add_student_to_indiv(callback: CallbackQuery, state: FSMContext):
    start_date = callback.data.split('_')[1]
    start_time = callback.data.split('_')[2]
    schedule_id = int(callback.data.split('_')[3])
    studio_name = callback.data.split('_')[4]
    studio_id = int(callback.data.split('_')[5])
    group_id = int(callback.data.split('_')[6])
    kb = await builders.show_all_students('addStudentToIndiv')

    await state.update_data(
        start_date=start_date, start_time=start_time,
        schedule_id=schedule_id, studio_name=studio_name,
        studio_id=studio_id, group_id=group_id
    )
    await callback.message.edit_text(
        'Выберите ученика для добавление в индивидуальное занятие'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('showStudentsToIndiv'))
async def show_student_to_indiv(callback: CallbackQuery):
    start_date = callback.data.split('_')[1]
    start_time = callback.data.split('_')[2]
    schedule_id = int(callback.data.split('_')[3])
    studio_name = callback.data.split('_')[4]
    studio_id = int(callback.data.split('_')[5])
    group_id = int(callback.data.split('_')[6])
    students = await student_service.get_students_from_group(group_id)
    if students:
        kb = inline.back_to_indiv_menu(
            start_date, start_time, schedule_id, group_id
        )
        list_students = '\n'.join([f'{student.name}' for student in students])

        await callback.message.edit_text(
            f'Список учеников\n{list_students}'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)
    else:
        kb = inline.select_schedule_to_studio_kb(
            start_date, start_time, schedule_id,
            studio_name, studio_id, group_id
        )
        await callback.message.edit_text(
            f'В {start_date} : {start_time} не добавлен ученик'
        )
        await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('delStudentToIndiv'))
async def step1_delete_student_to_indiv(
    callback: CallbackQuery,
    state: FSMContext
):
    start_date = callback.data.split('_')[1]
    start_time = callback.data.split('_')[2]
    schedule_id = int(callback.data.split('_')[3])
    studio_name = callback.data.split('_')[4]
    studio_id = int(callback.data.split('_')[5])
    group_id = int(callback.data.split('_')[6])
    kb = await builders.show_students_to_group('delStudentToIndiv2', group_id)

    await state.update_data(
        start_date=start_date, start_time=start_time,
        schedule_id=schedule_id, studio_name=studio_name,
        studio_id=studio_id, group_id=group_id
    )
    await callback.message.edit_text(
        'Выберите ученика для удаления из индвидуального занятия'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)
