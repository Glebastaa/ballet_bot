from aiogram.fsm.state import StatesGroup, State


class Studio(StatesGroup):
    name = State()


class Group(StatesGroup):
    group_name = State()
    studio_name = State()
    start_date = State()
    start_time = State()


class EditStudio(StatesGroup):
    new_studio_name = State()