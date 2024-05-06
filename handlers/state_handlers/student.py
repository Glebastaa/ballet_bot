import re

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from exceptions import EntityAlreadyExists
from services.student import StudentService
from utils.states import AddStudent, EditStudent
from keyboards import inline


router = Router()
student_service = StudentService()


@router.message(AddStudent.name)
async def step2_add_name_student(message: Message, state: FSMContext):
    student_name = message.text
    data = await state.get_data()
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')
    group_name = data.get('group_name')
    group_id = data.get('group_id')
    kb = inline.select_group_for_studio_kb(
        group_name, group_id, studio_name, studio_id
    )

    if re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', student_name):
        try:
            await student_service.add_student(student_name)
            await message.answer(
                f'Ученик {student_name} успешно добавлен\n'
                f'Выбрана группа {group_name}',
                reply_markup=kb
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
async def sted_edit_name_student(message: Message, state: FSMContext):
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
