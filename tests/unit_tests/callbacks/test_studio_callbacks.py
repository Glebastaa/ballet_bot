import pytest
from aiogram.types import CallbackQuery
from unittest.mock import AsyncMock, patch
from utils.states import EditStudio, Group
from callbacks.callbacks import (
    call_delete_studio, call_edit_studio,
    select_studio_for_group, select_studio,
    select_weekday_for_group,
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@pytest.mark.asyncio
async def test_call_edit_studio():
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = "select_studio_Шазам_123"
    state = AsyncMock()
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    await call_edit_studio(callback, state)

    # Assertions
    state.update_data.assert_awaited_once_with(studio_id=123, studio_name="Шазам")
    state.set_state.assert_awaited_once_with(EditStudio.new_studio_name)
    callback.message.edit_text.assert_awaited_once_with("Введите новое имя для студии Шазам")


@pytest.mark.asyncio
async def test_select_studio_for_group():
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = 'select_studio_Шазам_123'
    callback.message = AsyncMock()
    state = AsyncMock()
    state.get_data.return_value = {'group_name': 'БАБАДЖИ'}
    keyboard_mock = AsyncMock()

    with patch('keyboards.builders.create_weekdays_kb', return_value=keyboard_mock):
        await select_studio_for_group(callback, state)

    # Assertions
    state.update_data.assert_awaited_once_with(studio_name='Шазам', studio_id=123)
    callback.message.edit_text.assert_awaited_once_with('Студия Шазам выбрана. Выберите день недели занятия для группы БАБАДЖИ')
    callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=keyboard_mock)


@pytest.mark.asyncio
async def test_select_studio():
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = 'show_studio_Шазам_123'
    callback.message = AsyncMock()

    patch.object(callback.message, 'edit_text', autospec=True)
    patch.object(callback.message, 'edit_reply_markup', autospec=True)

    await select_studio(callback)

    callback.message.edit_text.assert_awaited_once_with('Выбрана студия Шазам')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить имя студии", callback_data="edit_studio_Шазам_123")],
        [InlineKeyboardButton(text="Удалить студию", callback_data="delete_studio_Шазам_123")],
        [InlineKeyboardButton(text="Список групп", callback_data="list_groups_Шазам_123")]
    ])
    callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=keyboard)


@pytest.mark.asyncio
async def test_delete_studio():
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = 'delete_studio_Шазам_123'
    callback.message = AsyncMock()
    patch("database.db_api.studio.delete_studio", autospec=True)
    patch.object(callback.message, "answer", autospec=True)
    session = AsyncMock()
    await call_delete_studio(callback, session)

    callback.message.answer.assert_awaited_once_with("Студия Шазам успешно удалена")


@pytest.mark.asyncio
async def test_select_weekday_for_group():
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = 'select_weekday_Понедельник'
    callback.message = AsyncMock()
    state = AsyncMock()
    state.update_date = AsyncMock()
    state.set_state = AsyncMock()
    state.get_data.return_value = {'group_name': 'БАБАДЖИ'}

    await select_weekday_for_group(callback, state)

    callback.message.answer.assert_awaited_once_with("Введите время начала занятия для группы БАБАДЖИ")
    state.set_state.assert_awaited_once_with(Group.start_time)
    callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=None)
