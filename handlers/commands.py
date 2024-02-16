from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import reply

router = Router()


@router.message(Command("add"))
async def add_main(message: Message, state: FSMContext):
    send_message = await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main)
    await state.update_data(last_bot_message_id=send_message.message_id)


@router.message(Command("show"))
async def show_main(message: Message, state: FSMContext):
    send_message = await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_info)
    await state.update_data(last_bot_message_id=send_message.message_id)


@router.message(Command("delete"))
async def delete_main(message: Message, state: FSMContext):
    send_message = await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_delete)
    await state.update_data(last_bot_message_id=send_message.message_id)


@router.message(Command("edit"))
async def edit_main(message: Message, state: FSMContext):
    send_message = await message.answer("Выебирте 1 из вариантов:", reply_markup=reply.main_edit)
    await state.update_data(last_bot_message_id=send_message.message_id)
