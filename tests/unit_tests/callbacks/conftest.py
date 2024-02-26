from unittest.mock import AsyncMock, MagicMock
import pytest
from aiogram.types import CallbackQuery


@pytest.fixture
def callback():
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    callback_query.message.edit_text = AsyncMock()
    callback_query.message.edit_reply_markup = AsyncMock()
    return callback_query


@pytest.fixture
def state():
    states = AsyncMock()
    states.update_data = AsyncMock()
    states.set_state = AsyncMock()
    states.get_data = AsyncMock()
    return states


@pytest.fixture
def session():
    sessions = AsyncMock()
    return sessions
