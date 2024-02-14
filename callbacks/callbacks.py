from aiogram.types import CallbackQuery
from aiogram import F, Router

from database.servise import delete_studio

router = Router()


@router.callback_query(F.data.startswith("show_studio_"))
async def select_studio(callback: CallbackQuery):
    studio_name = callback.data.split("_")[2]
    await callback.message.answer(f"Выбрана студия {studio_name}")


@router.callback_query(F.data.startswith("delete_studio_"))
async def call_delete_studio(callback: CallbackQuery):
    studio_name = callback.data.split("_")[2]
    result = await delete_studio(studio_name)
    if result:
        await callback.answer(f"Студия {studio_name} успешно удалена")
    else:
        await callback.answer(f"Студию {studio_name} не смогли удалить или она не существует")
