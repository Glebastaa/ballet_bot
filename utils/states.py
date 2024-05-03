from aiogram.fsm.state import StatesGroup, State


class Studio(StatesGroup):
    name = State()


class EditStudio(StatesGroup):
    name_update = State()
