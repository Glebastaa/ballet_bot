from aiogram.fsm.state import StatesGroup, State


class Studio(StatesGroup):
    name = State()


class Group(StatesGroup):
    group_name = State()
    studio_name = State()
    start_date = State()
    start_time = State()


class EditStudio(StatesGroup):
    studio_id = State()
    new_studio_name = State()


class EditGroup(StatesGroup):
    group_name = State()
    new_group_name = State()
    studio_name = State()


class Student(StatesGroup):
    name = State()


class AddStudent(StatesGroup):
    group_name = State()
    group_id = State()
    student_name = State()
    student_id = State()


class EditStudent(StatesGroup):
    student_name = State()
    student_id = State()
    new_student_name = State()


class AddIndiv(StatesGroup):
    studio_name = State()
    start_time = State()
    start_date = State()
