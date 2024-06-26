from aiogram.fsm.state import StatesGroup, State


class AddStudio(StatesGroup):
    name = State()


class EditStudio(StatesGroup):
    name_update = State()


class AddGroup(StatesGroup):
    name = State()
    start_time = State()
    test = State()


class EditGroup(StatesGroup):
    name = State()


class AddIndiv(StatesGroup):
    start_time = State()


class AddStudent(StatesGroup):
    name = State()


class EditStudent(StatesGroup):
    name = State()


class AddNotes(StatesGroup):
    notes = State()


class RegUser(StatesGroup):
    name = State()


class AdminPass(StatesGroup):
    password = State()
    switch_role = State()
