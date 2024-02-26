from typing import List
from aiogram.types import CallbackQuery
from aiogram import F, Router
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from database.db_api.individual_lesson import add_individual_lesson
from database.models import Student
from utils.states import AddIndiv, EditStudent, EditStudio, Group, EditGroup
from keyboards import builders, inline
from services.studio import StudioService
from services.group import GroupService
from services.student import StudentService


router = Router()
user_state = {}


def extract_data_from_callback(callback_query: CallbackQuery, index1=2, index2=3):
    data = callback_query.data.split("_")
    return data[index1], int(data[index2])


# Выбор студии и взаимодействие с ней
@router.callback_query(F.data.startswith("pick_studio_"))
async def call_select_studio(callback: CallbackQuery):
    studio_name, studio_id = extract_data_from_callback(callback)
    keyboard = inline.create_studio_kb(studio_name=studio_name, studio_id=studio_id)

    await callback.message.edit_text(f"Выбрана студия {studio_name}")
    await callback.message.edit_reply_markup(reply_markup=keyboard)


# Удаление студии
@router.callback_query(F.data.startswith("delete_studio_"))
async def call_delete_studio(callback: CallbackQuery) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)

    await StudioService().delete_studio(studio_id)
    await callback.message.answer(f"Студия {studio_name} успешно удалена")


# Изменение имени студии и передача на шаг new_studio_name
@router.callback_query(F.data.startswith("edit_studio_"))
async def call_edit_studio(callback: CallbackQuery, state: FSMContext) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)

    await state.update_data(studio_id=studio_id, studio_name=studio_name)
    await state.set_state(EditStudio.new_studio_name)
    await callback.message.edit_text(f"Введите новое имя для студии {studio_name}")


# Шаг 3 в создании группы. Выбор дня занятия
@router.callback_query(F.data.startswith("select_studio_"))
async def select_studio_for_group(callback: CallbackQuery, state: FSMContext) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)
    data = await state.get_data()
    group_name = data.get("group_name")

    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    await state.set_state(Group.start_date)
    await callback.message.edit_text(f"Студия {studio_name} выбрана. Выберите день недели занятия для группы {group_name}")
    await callback.message.edit_reply_markup(reply_markup=await builders.process_select_weekdays_kb())


# Шаг 4 в создании группы. Выбор времени занятия
@router.callback_query(F.data.startswith("select_weekday_"))
async def select_weekday_for_group(callback: CallbackQuery, state: FSMContext) -> None:
    start_date = callback.data.split("_")[2]
    data = await state.get_data()
    group_name = data.get("group_name")

    await state.update_data(start_date=start_date)
    await state.set_state(Group.start_time)
    await callback.message.answer(f"Введите время начала занятия для группы {group_name}")
    await callback.message.edit_reply_markup(reply_markup=None)


# Показ списка групп для студии
@router.callback_query(F.data.startswith("list_group_"))
async def call_list_groups(callback: CallbackQuery) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)
    groups = await GroupService().get_groups(studio_id)
    if not groups:
        await callback.message.edit_text(f"Увы, в студии {studio_name} пока нет групп. Пожалуйста, выберите другую студию.")
        await callback.message.edit_reply_markup("Выберите студию", reply_markup=await builders.process_show_list_groups())
        return

    await callback.message.edit_text(f"Список групп для студии {studio_name}")
    await callback.message.edit_reply_markup(reply_markup=await builders.show_list_groups_for_studio(studio_name, studio_id))


# Выбор группы и взаимодействие с ней
@router.callback_query(F.data.startswith("pick_group_"))
async def select_group_for_studio(callback: CallbackQuery) -> None:
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split("_")[4]
    keyboard = inline.select_group_for_studio_kb(group_name, group_id, studio_name)

    await callback.message.edit_text(f"Выбрана группа {group_name}")
    await callback.message.edit_reply_markup(reply_markup=keyboard)


# Удаление группы
@router.callback_query(F.data.startswith("delete_group_"))
async def call_delete_group(callback: CallbackQuery) -> None:
    group_name, group_id = extract_data_from_callback(callback)

    await GroupService().delete_group(group_id)
    await callback.message.answer(f"Группа {group_name} успешно удалена")


# Изменение имени группы и передача на шаг new_group_name
@router.callback_query(F.data.startswith("edit_group_"))
async def call_edit_group(callback: CallbackQuery, state: FSMContext) -> None:
    group_name, group_id = extract_data_from_callback(callback)
    studio_name = callback.data.split("_")[4]

    await state.update_data(group_name=group_name, group_id=group_id)
    await state.set_state(EditGroup.new_group_name)
    await callback.message.edit_text(f"Студия: {studio_name}\nВведите новое имя для группы {group_name}")
    await callback.message.edit_reply_markup(reply_markup=None)


# Список групп для выбранной студии
@router.callback_query(F.data.startswith("list_studios_"))
async def call_list_studios(callback: CallbackQuery) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)

    await callback.message.edit_text(f"Список групп для студии {studio_name}")
    await callback.message.edit_reply_markup(reply_markup=await builders.process_edit_group_name(studio_name, studio_id))


# Выбор ученика для дальнешего взаимодействия
@router.callback_query(F.data.startswith("pick_student_"))
async def select_students(callback: CallbackQuery) -> None:
    student_name, student_id = extract_data_from_callback(callback)
    keyboard = inline.select_students_kb(student_name, student_id)

    await callback.message.edit_text(f"Выбран ученик - {student_name}")
    await callback.message.edit_reply_markup(reply_markup=keyboard)


# Выбор ученика для добавления в группу
@router.callback_query(F.data.startswith("add_student_"))
async def call_add_student_to_group(callback: CallbackQuery, state: FSMContext) -> None:
    group_name, group_id = extract_data_from_callback(callback)

    await state.update_data(group_name=group_name, group_id=group_id)
    await callback.message.edit_text(f"Выберите ученика для добавления его в группу {group_name}")
    await callback.message.edit_reply_markup(reply_markup=await builders.process_add_student_to_group())


# Добавление ученика в группу
@router.callback_query(F.data.startswith("add_student2_"))
async def select_student_for_group(callback: CallbackQuery, state: FSMContext) -> None:
    student_name, student_id = extract_data_from_callback(callback)
    data = await state.get_data()
    group_name: str = data.get("group_name", "Проблема")
    group_id: int = data.get("group_id", -1)

    await StudentService().add_student_to_group(student_id, group_id)
    await callback.message.edit_text(f"Ученик {student_name} успешно добавлен в группу {group_name}")
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.clear()


# Показ списка учеников для группы
@router.callback_query(F.data.startswith("list_students_"))
async def call_list_students(callback: CallbackQuery) -> None:
    group_name, group_id = extract_data_from_callback(callback)
    students = await StudentService().get_students_from_group(group_id)

    if not students:
        await callback.message.edit_text(f"Учеников нет в группе {group_name}. Выберите другую группу")
        await callback.message.edit_reply_markup(reply_markup=await builders.process_show_list_groups())
        return

    await callback.message.edit_text(f"Список учеников для группы {group_name}")
    await callback.message.edit_reply_markup(reply_markup=await builders.show_student_to_group_menu(group_id))


# Удаление ученика из БД
@router.callback_query(F.data.startswith("delete_student_"))
async def call_delete_student_from_group(callback: CallbackQuery) -> None:
    student_name, student_id = extract_data_from_callback(callback)

    await StudentService().delete_student(student_id)
    await callback.message.answer(f"Ученик {student_name} успешно удален")


# Редактирование имени ученика
@router.callback_query(F.data.startswith("edit_student_"))
async def call_edit_student_name(callback: CallbackQuery, state: FSMContext) -> None:
    student_name, student_id = extract_data_from_callback(callback)

    await state.update_data(student_name=student_name, student_id=student_id)
    await state.set_state(EditStudent.new_student_name)
    await callback.message.edit_text(f"Введите новое имя ученика {student_name}")
    await callback.message.edit_reply_markup(reply_markup=None)


# Выбор студии для добавления индива с переходом в выбор start_time
@router.callback_query(F.data.startswith("add_indiv_"))
async def call_add_indiv_to_studio(callback: CallbackQuery, state: FSMContext) -> None:
    studio_name, studio_id = extract_data_from_callback(callback)

    await state.update_data(studio_name=studio_name, studio_id=studio_id)
    await state.set_state(AddIndiv.start_time)
    await callback.message.answer(f"Введите время начала занятия для индива в студии - {studio_name}")
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith("weekday_indiv_"))
async def select_weekday_for_indiv(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    start_date = callback.data.split("_")[2]
    data = await state.get_data()
    studio_name: str = data.get("studio_name", "Проблема")
    studio_id: int = data.get("studio_id", -1)
    start_time = data.get("start_time", "00:00")

    await add_individual_lesson(session, studio_id, start_time, start_date)
    await callback.message.answer(f"Индивидуальное занятие для студии {studio_name} успешно добавлено по {start_date} в {start_time}")
    await state.clear()
