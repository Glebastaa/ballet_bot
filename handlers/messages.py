from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import builders
from utils.states import AddStudent, AddStudio
from middlewares.decorator import registered_user_required, roles_user_required


router = Router()


@router.message(F.text.lower() == 'добавить студию')
@registered_user_required
@roles_user_required(['owner'])
async def form_add_studio(message: Message, state: FSMContext):
    await state.set_state(AddStudio.name)
    await message.answer('Введите название студии:')


@router.message(F.text.lower() == 'студии')
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def form_list_studios(message: Message):
    await message.answer(
        'Список студий:',
        reply_markup=await builders.show_list_studios_menu(
            action='selectStudio'
        )
    )


@router.message(F.text.lower() == 'добавить ученика')
@registered_user_required
@roles_user_required(['owner'])
async def form_add_student(message: Message, state: FSMContext):
    await state.set_state(AddStudent.name)
    await message.answer('Введите имя ученика:')


@router.message(F.text.lower() == 'ученик')
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def form_select_student(message: Message):
    await message.answer(
        'Список учеников:',
        reply_markup=await builders.show_all_students(action='listStudents')
    )
