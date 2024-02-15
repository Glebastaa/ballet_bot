from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F, Router
from sqlalchemy.ext.asyncio import AsyncSession

from database.servise import delete_studio, edit_studio

router = Router()
user_state = {}


@router.callback_query(F.data.startswith("show_studio_"))
async def select_studio(callback: CallbackQuery):
    studio_name = callback.data.split("_")[2]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить имя студии", callback_data=f"edit_studio_{studio_name}")
            ],
            [
                InlineKeyboardButton(text="Удалить студию", callback_data=f"delete_studio_{studio_name}")
            ]
        ],
    )
    await callback.message.answer(f"Выбрана студия {studio_name}", reply_markup=keyboard)


@router.callback_query(F.data.startswith("delete_studio_"))
async def call_delete_studio(callback: CallbackQuery, session: AsyncSession):
    studio_name = callback.data.split("_")[2]
    result = await delete_studio(session, studio_name)
    if result:
        await callback.message.answer(f"Студия {studio_name} успешно удалена")
    else:
        await callback.message.answer(f"Студию {studio_name} не смогли удалить или она не существует")


@router.callback_query(F.data.startswith("edit_studio_"))
async def call_edit_studio(callback: CallbackQuery, session: AsyncSession):
    studio_name = callback.data.split("_")[2]
    user_state[callback.from_user.id] = studio_name
    await callback.message.answer(f"Введите новое имя для студии {studio_name}.")


@router.message()
async def message_handler(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    if user_id in user_state:
        studio_name = user_state[user_id]
        new_studio_name = message.text
        result = await edit_studio(session, studio_name, new_studio_name)
        if result:
            await message.answer(f"Студия {studio_name} успешно изменена на {new_studio_name}")
        else:
            await message.answer(f"Студию {studio_name} не удалось изменить или она не существует")

        del user_state[user_id]
