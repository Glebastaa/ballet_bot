from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import builders
from utils.states import Studio


router = Router()

@router.message(F.text.lower() == "добавить студию")
async def form_add_studio(message: Message, state: FSMContext):
    await state.set_state(Studio.name)
    await message.answer("Введите название студии:")


@router.message(F.text.lower() == "список студий")
async def message_list_studios(message: Message):
    await message.answer(
        "Список студий:",
        reply_markup=await builders.show_list_studios_menu('listStudio')
    )


@router.message(F.text.lower() == "удалить студию")
async def message_delete_studio(message: Message):
    await message.answer(
        "Выберите студию для удаления:",
        reply_markup=await builders.show_delete_studios_menu()
    )


@router.message(F.text.lower() == "изменить имя студии")
async def form_change_name_studio(message: Message):
    await message.answer(
        "Выберите студию для изменения имени:",
        reply_markup=await builders.show_edit_studios_menu()
    )


@router.message(F.text.lower() == "добавить группу")
async def form_add_group(message: Message, state: FSMContext):
    await state.set_state(Group.group_name)
    await message.answer("Введите название группы:")


@router.message(F.text.lower() == "список групп")
async def message_list_groups(message: Message):
    await message.answer(
        "Выберите студию, в которой хотите просмотреть группы",
        reply_markup=await builders.process_show_list_groups()
    )


@router.message(F.text.lower() == "изменить имя группы")
async def form_change_name_group(message: Message):
    await message.answer(
        "Выберите студию, в которой хотите сменить название группы:",
        reply_markup=await builders.process_edit_group_name_for_studio()
    )


@router.message(F.text.lower() == "добавить ученика")
async def form_add_student(message: Message, state: FSMContext):
    await state.set_state(Student.name)
    await message.answer("Введите имя ученика:")


@router.message(F.text.lower() == "список учеников")
async def form_add_student_to_group(message: Message):
    await message.answer(
        "Список учеников:",
        reply_markup=await builders.show_list_students_menu()
    )


@router.message(F.text.lower() == "добавить индив")
async def form_add_indiv(message: Message):
    await message.answer(
        "Выберите студию, в которой хотите добавить индивидуальный занятие",
        reply_markup=await builders.process_add_indiv_to_studio()
    )
