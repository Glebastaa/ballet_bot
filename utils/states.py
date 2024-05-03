from aiogram.fsm.state import StatesGroup, State


class AddStudio(StatesGroup):
    name = State()


class EditStudio(StatesGroup):
    name_update = State()


class AddGroup(StatesGroup):
    name = State()
    start_time = State()
    test = State()
