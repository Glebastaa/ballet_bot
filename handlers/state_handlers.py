import re
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from exceptions import EntityAlreadyExists
from utils.states import EditStudio, Studio
from services.studio import StudioService


router = Router()


@router.message(Studio.name)
async def step_add_name_studio(message: Message, state: FSMContext):
    "Check and add studio to table studios"
    studio_name = message.text

    if re.match(r'^[а-яА-ЯёЁ\s]+$', message.text):
        try:
            await StudioService().add_studio(studio_name)
            await message.answer(f'Студия {studio_name} успешно добавлена!')
            await state.clear()
        except EntityAlreadyExists:
            await message.answer(
                f'Студия {studio_name} уже существует.'
                'Попробуйте ввести другое название.'
            )
    else:
        await message.answer(
            'Пожалуйста, введите имя группы корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(EditStudio.name_update)
async def step_edit_name_studio(message: Message, state: FSMContext):
    "Check and edit name studio"
    new_name = message.text
    data = await state.get_data()
    studio_name = data.get('studio_name')
    studio_id = data.get('studio_id')

    if new_name == studio_name:
        await message.answer(
            'Имя студии не может быть таким же, как '
            'и до этого. Попробуйте снова'
        )
    elif re.match(r'^[а-яА-ЯёЁ0-9\s]+$', new_name):
        await StudioService().edit_studio(studio_id, new_name)
        await message.answer(
            f'Студия {studio_name} успешно изменена на {new_name}'
        )
        await state.clear()
    else:
        await message.answer(
            'Пожалуйста, введите имя студии корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )
