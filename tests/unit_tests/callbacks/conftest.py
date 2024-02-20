from unittest.mock import AsyncMock, MagicMock
import pytest
from aiogram.types import CallbackQuery


@pytest.fixture
def callback():
    callback_query = MagicMock(spec=CallbackQuery)
    callback_query.message = AsyncMock()
    yield callback_query


@pytest.fixture
def state():
    state = AsyncMock()
    yield state
