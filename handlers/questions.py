import re
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from exceptions import EntityAlreadyExists
from keyboards import builders
from utils.states import AddIndiv, EditStudent, EditStudio, Studio, Group, EditGroup, Student
from services.studio import StudioService
from services.group import GroupService
from services.student import StudentService


router = Router()


@router.message(Studio.name)
async def form_name_studio(message: Message, state: FSMContext):
    studio_name = message.text

    if re.match(r'^[а-яА-ЯёЁ\s]+$', message.text):
        try:
            await StudioService().add_studio(studio_name)
            await message.answer(f"Студия {studio_name} успешно добавлена")
            await state.clear()
        except EntityAlreadyExists:
            await message.answer(f"Студия {studio_name} уже существует. Попробуйте ввести другое название.")

    else:
        await message.answer("Пожалуйста, введите имя студии корректно, используя только русские буквы. Попробуйте снова:")


# Шаг 2 в создании группы. Выбор студии
@router.message(Group.group_name)
async def form_name_group(message: Message, state: FSMContext):
    group_name = message.text

    if re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', group_name):
        try:
            await state.update_data(group_name=message.text)
            await state.set_state(Group.studio_name)
            await message.answer(f"Выберите студию для группы {group_name}", reply_markup=await builders.process_select_studio_for_group())
        except EntityAlreadyExists:
            await message.answer(f"Группа {group_name} уже существует. Попробуйте ввести другое название.")

    else:
        await message.answer("Пожалуйста, введите имя группы корректно, используя только русские буквы. Попробуйте снова:")


# Шаг 5 в создании группы. Финал
@router.message(Group.start_time)
async def form_end_add_group(message: Message, state: FSMContext):
    start_time_str = str(message.text)
    data = await state.get_data()
    group_name = str(data.get("group_name"))
    studio_name = data.get("studio_name")
    start_date = data.get("start_date")
    studio_id = data.get("studio_id")

    try:
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
    except ValueError:
        await message.answer("Время введено неверно. Пожалуйста, введите время в формате HH:MM.")
        return

    await GroupService().add_group(group_name, studio_id, start_time, start_date)
    await message.answer(f"Группа {group_name} успешно добавлена в студию {studio_name} с временем начала в {start_date} : {start_time}")
    await state.clear()


@router.message(EditGroup.new_group_name)
async def form_new_group_name(message: Message, state: FSMContext):
    new_group_name = message.text
    data = await state.get_data()
    group_name = data.get("group_name")
    group_id = data.get("group_id")

    if new_group_name == group_name:
        await message.answer("Имя группы не может быть таким же, как и до этого. Попробуйте снова")

    elif re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', new_group_name):
        await GroupService().edit_group(group_id, new_group_name)
        await message.answer(f"Группа {group_name} успешно изменена на {new_group_name}")
        await state.clear()

    else:
        await message.answer("Пожалуйста, введите имя группы корректно, используя только русские буквы. Попробуйте снова:")


@router.message(EditStudio.new_studio_name)
async def form_new_studio_name(message: Message, state: FSMContext):
    new_studio_name = message.text
    data = await state.get_data()
    studio_name = data.get("studio_name")
    studio_id = data.get("studio_id")

    if new_studio_name == studio_name:
        await message.answer("Имя студии не может быть таким же, как и до этого. Попробуйте снова")

    elif re.match(r'^[а-яА-ЯёЁ0-9\s]+$', new_studio_name):
        await StudioService().edit_studio(studio_id, new_name=new_studio_name)
        await message.answer(f"Студия {studio_name} успешно изменена на {new_studio_name}")
        await state.clear()

    else:
        await message.answer("Пожалуйста, введите имя студии корректно, используя только русские буквы. Попробуйте снова:")


@router.message(Student.name)
async def form_name_student(message: Message, state: FSMContext):
    student_name = message.text
    await StudentService().add_student(student_name)
    await message.answer(f"Ученик {student_name} успешно добавлен")
    await state.clear()


@router.message(EditStudent.new_student_name)
async def form_edit_student_name(message: Message, state: FSMContext):
    new_student_name = message.text
    data = await state.get_data()
    student_name: str = data.get("student_name")
    student_id: int = data.get("student_id")

    if new_student_name == student_name:
        await message.answer("Имя ученика не может быть таким же, как и до этого. Попробуйте снова")
    elif re.match(r'^[а-яА-ЯёЁ0-9\s]+$', new_student_name):
        await StudentService().edit_student(student_id, new_name=new_student_name)
        await message.answer(f"Ученик {student_name} успешно изменен на {new_student_name}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, введите имя ученика корректно, используя только русские буквы. Попробуйте снова:")


@router.message(AddIndiv.start_time)
async def form_add_time_indiv(message: Message, state: FSMContext):
    start_time_str = str(message.text)
    data = await state.get_data()
    studio_name = data.get("studio_name")

    try:
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
    except ValueError:
        await message.answer("Время введено неверно. Пожалуйста, введите время в формате HH:MM.")
        return

    await state.update_data(start_time=start_time)
    await state.set_state(AddIndiv.start_date)
    await message.answer(f"Выбери день, когда будет проходить занятие в студии {studio_name}", reply_markup=await builders.process_select_weekdays_indiv())
