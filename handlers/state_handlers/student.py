import re

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from exceptions import EntityAlreadyExists
from services.student import StudentService
from utils.states import AddStudent, EditStudent


router = Router()
student_service = StudentService()


@router.message(AddStudent.name)
async def add_name_student(message: Message, state: FSMContext):
    "Check student name and add student"
    student_name = message.text

    if re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', student_name):
        try:
            await student_service.add_student(student_name)
            await message.answer(
                f'Ученик {student_name} успешно добавлен',
                reply_markup=None
            )
            await state.clear()
        except EntityAlreadyExists:
            await message.answer(
                f'Студен {student_name} уже существует. '
                'Попробуйте ввести другое имя.'
            )
    else:
        await message.answer(
            'Пожалуйста, введите имя учени корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(EditStudent.name)
async def step_edit_name_student(message: Message, state: FSMContext):
    "Check student name and edit student"
    new_name = message.text
    data = await state.get_data()
    student_name = data.get('student_name')
    student_id = data.get('student_id')

    if new_name == student_name:
        await message.answer(
            'Имя ученика не может быть таким же, '
            'как и до этого. Попробуйте снова'
        )
    elif re.match(r'^[а-яА-ЯёЁ0-9\s]+$', new_name):
        await student_service.edit_student(student_id, new_name)
        await message.answer(
            f'Ученик {student_name} успешно изменен на {new_name}'
        )
        await state.clear()
    else:
        await message.answer(
            'Пожалуйста, введите имя ученика корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )
