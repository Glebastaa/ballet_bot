from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F, Router
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from database.models import Studio
from utils.states import Group, EditGroup
from keyboards import builders

from database.db_api.group import get_groups, delete_group
from database.db_api.studio import delete_studio, edit_studio, get_by_name

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
            ],
            [
                InlineKeyboardButton(text="Список групп", callback_data=f"list_groups_{studio_name}")
            ]
        ],
    )
    await callback.message.edit_text(f"Выбрана студия {studio_name}")
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data.startswith("delete_studio_"))
async def call_delete_studio(callback: CallbackQuery, session: AsyncSession):
    studio_name = callback.data.split("_")[2]
    studio = await get_by_name(Studio, studio_name, session)
    if studio:
        await delete_studio(session, studio)

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


@router.callback_query(F.data.startswith("select_studio_"))
async def select_studio_for_group(callback: CallbackQuery, state: FSMContext):
    studio_name = callback.data.split("_")[2]
    await state.update_data(studio_name=studio_name)
    data = await state.get_data()
    group_name = data.get("group_name")
    await callback.message.edit_text(f"Студия {studio_name} выбрана. Выберите день недели занятия для группы {group_name}")
    await callback.message.edit_reply_markup(reply_markup=await builders.create_weekdays_kb())   


@router.callback_query(F.data.startswith("select_weekday_"))
async def select_weekday_for_group(callback: CallbackQuery, state: FSMContext):
    start_date = callback.data.split("_")[2]
    await state.update_data(start_date=start_date)
    data = await state.get_data()
    group_name = data.get("group_name")
    await state.set_state(Group.start_time)
    await callback.message.answer(f"Введите время начала занятия для группы {group_name}")
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith("list_groups_"))
async def call_list_groups(callback: CallbackQuery, session: AsyncSession):
    studio_name = callback.data.split("_")[2]
    await callback.message.edit_text(f"Список групп для студии {studio_name}")
    await callback.message.edit_reply_markup(reply_markup=await builders.get_groups_for_studio(studio_name, session))


@router.callback_query(F.data.startswith("select_group_"))
async def select_group_for_studio(callback: CallbackQuery):
    group_name = callback.data.split("_")[2]
    studio_name = callback.data.split("_")[3]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить имя группы", callback_data=f"edit_group_{group_name}_{studio_name}")
            ],
            [
                InlineKeyboardButton(text="Удалить группу", callback_data=f"delete_group_{group_name}_{studio_name}")
            ],
        ],
    )
    await callback.message.edit_text(f"Выбрана группа {group_name}")
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data.startswith("delete_group_"))
async def call_delete_group(callback: CallbackQuery, session: AsyncSession):
    group_name = callback.data.split("_")[2]
    studio_name = callback.data.split("_")[3]
    group = await get_groups(session, studio_name)
    if group:
        await delete_group(session, group_name, studio_name)
        await callback.message.answer(f"Группа {group_name} успешно удалена")
    else:
        await callback.message.answer(f"Группу {group_name} не смогли удалить или она не существует")


@router.callback_query(F.data.startswith("edit_group_"))
async def call_edit_group(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    group_name = callback.data.split("_")[2]
    studio_name = callback.data.split("_")[3]
    await state.update_data(group_name=group_name, studio_name=studio_name)
    await state.set_state(EditGroup.new_group_name)
    await callback.message.edit_text(f"Студия: {studio_name}\nВведите новое имя для группы {group_name}")
    await callback.message.edit_reply_markup(reply_markup=None)
