# from aiogram.types import CallbackQuery
# from unittest.mock import AsyncMock, patch
# from utils.states import EditStudio, Group
# from callbacks.callbacks import (
#     call_delete_studio, call_edit_studio, call_list_groups, select_group_for_studio,
#     select_studio_for_group, select_studio,
#     select_weekday_for_group,
# )
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# async def test_call_edit_studio(callback, state):
#     callback.data = "select_studio_Шазам_123"

#     await call_edit_studio(callback, state)

#     # Ассерты
#     state.update_data.assert_awaited_once_with(studio_id=123, studio_name="Шазам")
#     state.set_state.assert_awaited_once_with(EditStudio.new_studio_name)
#     callback.message.edit_text.assert_awaited_once_with("Введите новое имя для студии Шазам")


# async def test_select_studio_for_group(callback, state):
#     callback.data = "select_studio_Шазам_123"
#     state.get_data.return_value = {"group_name": "БАБАДЖИ"}
#     keyboard_mock = AsyncMock()

#     with patch("keyboards.builders.create_weekdays_kb", return_value=keyboard_mock):
#         await select_studio_for_group(callback, state)

#     # Ассерты
#     state.update_data.assert_awaited_once_with(studio_name="Шазам", studio_id=123)
#     callback.message.edit_text.assert_awaited_once_with("Студия Шазам выбрана. Выберите день недели занятия для группы БАБАДЖИ")
#     callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=keyboard_mock)


# async def test_select_studio(callback):
#     callback.data = "show_studio_Шазам_123"

#     patch.object(callback.message, "edit_text", autospec=True)
#     patch.object(callback.message, "edit_reply_markup", autospec=True)

#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Изменить имя студии", callback_data="edit_studio_Шазам_123")],
#         [InlineKeyboardButton(text="Удалить студию", callback_data="delete_studio_Шазам_123")],
#         [InlineKeyboardButton(text="Список групп", callback_data="list_groups_Шазам_123")]
#     ])

#     await select_studio(callback)

#     # Ассерты
#     callback.message.edit_text.assert_awaited_once_with("Выбрана студия Шазам")
#     callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=keyboard)


# async def test_delete_studio(callback, session):
#     callback.data = "delete_studio_Шазам_123"

#     patch("database.db_api.studio.delete_studio", autospec=True)
#     patch.object(callback.message, "answer", autospec=True)

#     await call_delete_studio(callback, session)

#     # Ассерты
#     callback.message.answer.assert_awaited_once_with("Студия Шазам успешно удалена")


# async def test_select_weekday_for_group(callback, state):
#     callback.data = "select_weekday_Понедельник"
#     state.get_data.return_value = {"group_name": "БАБАДЖИ"}

#     await select_weekday_for_group(callback, state)

#     # Ассерты
#     callback.message.answer.assert_awaited_once_with("Введите время начала занятия для группы БАБАДЖИ")
#     state.set_state.assert_awaited_once_with(Group.start_time)
#     callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=None)


# async def test_call_list_groups(callback, session):
#     callback.data = "list_groups_Шазам_123"
#     keyboard = AsyncMock()

#     with patch('keyboards.builders.get_groups_for_studio', return_value=keyboard):
#         await call_list_groups(callback, session)

#         # Ассерты
#         callback.message.edit_text.assert_awaited_once_with("Список групп для студии Шазам")
#         callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=keyboard)


# async def test_select_group_for_studio(callback):
#     callback.data = "select_group_БАБАДЖИ_123_Шазам"
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Сменить имя группы", callback_data="edit_group_БАБАДЖИ_123_Шазам")],
#         [InlineKeyboardButton(text="Удалить группу", callback_data="delete_group_БАБАДЖИ_123")],
#     ])

#     await select_group_for_studio(callback)

#     # Ассерты
#     callback.message.edit_text.assert_awaited_once_with("Выбрана группа БАБАДЖИ")
#     callback.message.edit_reply_markup.assert_awaited_once_with(reply_markup=keyboard)
