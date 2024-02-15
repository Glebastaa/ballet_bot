from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import builders
from sqlalchemy.ext.asyncio import AsyncSession
from utils.states import Studio, Group


router = Router()

@router.message(F.text.lower() == "добавить студию")
async def form_add_studio(message: Message, state: FSMContext):
    await state.set_state(Studio.name)
    await message.answer("Введите название студии:")


@router.message(F.text.lower() == "список студий")
async def message_list_studios(message: Message, session: AsyncSession):
    await message.answer(
        "Список студий:",
        reply_markup=await builders.get_studios_kb(session=session)
    )


@router.message(F.text.lower() == "удалить студию")
async def message_delete_studio(message: Message, session: AsyncSession):
    await message.answer(
        "Выберите студию для удаления:",
        reply_markup=await builders.delete_studios_kb(session=session)
    )


@router.message(F.text.lower() == "изменить имя студии")
async def form_change_name_studio(message: Message, session: AsyncSession):
    await message.answer(
        "Выберите студию для изменения имени:",
        reply_markup=await builders.edit_studios_kb(session=session)
    )


@router.message(F.text.lower() == "добавить группу")
async def form_add_group(message: Message, state: FSMContext):
    await state.set_state(Group.group_name)
    await message.answer("Введите название группы:")
