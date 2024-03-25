import re
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from schemas.group import GroupSchema
from database.models import WeekDays, UserRoles
from exceptions import (
    EntityAlreadyExists,
    ScheduleTimeInsertionError,
    UserAlreadyExistsError
)
from bots.keyboards import builders, inline
from utils.states import (
    AddIndiv, AdminPass, EditStudent,
    EditStudio, Studio,
    Group, EditGroup,
    Student, RegUser)
from services.studio import StudioService
from services.group import GroupService
from services.student import StudentService
from services.user import UserService


router = Router()
ADMIN_PASS = '4321'
studio_service = StudioService()
group_service = GroupService()
student_service = StudentService()
user_service = UserService()


@router.message(Studio.name)
async def form_name_studio(message: Message, state: FSMContext):
    studio_name: str = message.text  # type: ignore

    if re.match(r'^[а-яА-ЯёЁ\s]+$', studio_name):
        try:
            await studio_service.add_studio(studio_name)
            await message.answer(
                f'Студия {studio_name} успешно добавлена. '
            )
            await state.clear()
        except EntityAlreadyExists:
            await message.answer(
                f'Студия {studio_name} уже существует. '
                'Попробуйте ввести другое название.'
            )

    else:
        await message.answer(
            'Пожалуйста, введите имя студии корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(EditStudio.new_studio_name)
async def form_new_studio_name(message: Message, state: FSMContext):
    new_studio_name: str = str(message.text)
    data = await state.get_data()
    studio_name = data.get('studio_name')
    studio_id: int = data.get('studio_id')  # type: ignore

    if new_studio_name == studio_name:
        await message.answer(
            'Имя студии не может быть таким же, '
            'как и до этого. Попробуйте снова'
        )

    elif re.match(r'^[а-яА-ЯёЁ0-9\s]+$', new_studio_name):  # type: ignore
        await studio_service.edit_studio(studio_id, new_name=new_studio_name)
        await message.answer(
            f'Студия {studio_name} успешно изменена на {new_studio_name}'
        )
        await state.clear()

    else:
        await message.answer(
            'Пожалуйста, введите имя студии корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


# Шаг 2 в создании группы. Выбор студии
@router.message(Group.group_name)
async def form_name_group(message: Message, state: FSMContext):
    group_name = message.text
    keyboard = await builders.show_list_studios_menu(action='select_studio')

    if re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', group_name):  # type: ignore
        try:
            await state.update_data(group_name=group_name)
            await message.answer(
                f'Выберите студию для группы {group_name}',
                reply_markup=keyboard,
            )
        except EntityAlreadyExists:
            await message.answer(
                f'Группа {group_name} уже существует. '
                'Попробуйте ввести другое название.'
            )

    else:
        await message.answer(
            'Пожалуйста, введите имя группы корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(Group.start_time)
async def form_end_add_group(message: Message, state: FSMContext):
    start_time_str = str(message.text)
    data = await state.get_data()
    studio_name: str = data.get('studio_name', 'problem')
    studio_id: int = data.get('studio_id', 1)
    group_name: str = data.get('group_name', 'problem')
    start_date: WeekDays = data.get('start_date')  # type: ignore
    group = await group_service.add_group(
            group_name, studio_id, is_individual=False
        )

    try:
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        await group_service.add_schedule_to_group(
            group_id=group.id,
            start_time=start_time,
            start_date=start_date
        )
        await message.answer(
            f'Добавлено расписание день - {start_date.value}, время - '
            f'{start_time} для группы {group.name} в студии {studio_name}'
        )
        await state.clear()
    except ValueError:
        await message.answer(
            'Время введено неверно. Пожалуйста, введите время в формате HH:MM.'
        )
        return
    except ScheduleTimeInsertionError:
        await message.answer(
            f'Невозможно добавить расписание. Время {start_time} уже занято '
            f'или слишком близко к существующему расписанию.'
        )


@router.message(EditGroup.new_group_name)
async def form_new_group_name(message: Message, state: FSMContext):
    new_group_name: str = str(message.text)
    data = await state.get_data()
    group_name = data.get('group_name')
    group_id: int = data.get('group_id')  # type: ignore

    if new_group_name == group_name:
        await message.answer(
            'Имя группы не может быть таким же, как и до этого. '
            'Попробуйте снова'
        )

    elif re.match(r'^[а-яА-ЯёЁ0-9\s\-]+$', new_group_name):  # type: ignore
        await GroupService().edit_group(group_id, new_group_name)
        await message.answer(
            f'Группа {group_name} успешно изменена на {new_group_name}'
        )
        await state.clear()

    else:
        await message.answer(
            'Пожалуйста, введите имя группы корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(Student.name)
async def form_name_student(message: Message, state: FSMContext):
    student_name: str = str(message.text)
    await StudentService().add_student(student_name)
    await message.answer(f'Ученик {student_name} успешно добавлен')
    await state.clear()


@router.message(EditStudent.new_student_name)
async def form_edit_student_name(message: Message, state: FSMContext):
    new_name: str = str(message.text)
    data = await state.get_data()
    student_name: str = str(data.get('student_name'))
    student_id: int = data.get('student_id')  # type: ignore

    if new_name == student_name:
        await message.answer(
            'Имя ученика не может быть таким же, '
            'как и до этого. Попробуйте снова'
        )
    elif re.match(r'^[а-яА-ЯёЁ0-9\s]+$', new_name):
        await StudentService().edit_student(student_id, new_name)
        await message.answer(
            f'Ученик {student_name} успешно изменен на {new_name}'
        )
        await state.clear()
    else:
        await message.answer(
            'Пожалуйста, введите имя ученика корректно, '
            'используя только русские буквы. Попробуйте снова:'
        )


@router.message(AddIndiv.start_time)
async def form_add_time_indiv(message: Message, state: FSMContext):
    start_time_str = str(message.text)
    data = await state.get_data()
    indiv: GroupSchema = data.get('indiv')  # type: ignore
    studio_name: str = data.get('studio_name', '1')
    start_date: WeekDays = data.get('start_date')  # type: ignore

    try:
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        await GroupService().add_schedule_to_group(
            group_id=indiv.id,
            start_time=start_time,
            start_date=start_date
        )
        await message.answer(
            f'Индивидуальное занятие в студии {studio_name} '
            f'в {start_date.value} : {start_time} добавленно в рассписание'
        )
        await state.clear()
    except ValueError:
        await message.answer(
            'Время введено неверно. Пожалуйста, введите время в формате HH:MM.'
        )
        return
    except ScheduleTimeInsertionError:
        await message.answer(
            f'Невозможно добавить расписание. Время {start_time} уже занято '
            f'или слишком близко к существующему расписанию.'
        )


@router.message(RegUser.wait_for_name)
async def set_username(message: Message, state: FSMContext):
    username: str = str(message.text)
    curr_id = message.from_user.id

    try:
        new_user = await UserService().register_user(
            telegram_id=curr_id,
            username=username
        )
        await message.answer(
            f'Вы зарегестрировались как {new_user.username}'
        )
        await state.clear()
    except UserAlreadyExistsError:
        await message.answer(
            f'Пользователь с именем {username} уже зарегестрирован'
        )


@router.message(AdminPass.wait_for_pass)
async def check_admin_pass(message: Message, state: FSMContext):
    check_pass = message.text
    if check_pass == ADMIN_PASS:
        user_id = message.from_user.id
        role = UserRoles.OWNER
        await UserService().switch_to_another_role(
            telegram_id=user_id, role=role
        )
        await message.answer(
            'Вы вошли в панель администратора. Выберите действие',
            reply_markup=inline.show_admin_menu_kb()
        )
    else:
        await message.answer('Неверный пароль, попробуйте еще раз')
    await state.clear()


# TODO Доделать при появлении функции получения id и получения bool
@router.message(AdminPass.switch_role)
async def switch_role(message: Message, state: FSMContext):
    user_name: str = str(message.text)
    user_id = await UserService().get_user_id_by_username(username=user_name)
    if user_id:
        data = await state.get_data()
        switch_role: UserRoles = data.get('switch_role')  # type: ignore
        await UserService().switch_to_another_role(
            telegram_id=user_id, role=switch_role
        )
        await message.answer(
            f'Роль для {user_name} изменена на {switch_role.value}'
        )
        await message.answer(
            'Выберите действие',
            reply_markup=inline.show_admin_menu_kb()
        )
        await state.clear()
    else:
        await message.answer(
            f'Пользователь {user_name} не найден. '
            'Попробуйте ввести логин еще раз'
        )
