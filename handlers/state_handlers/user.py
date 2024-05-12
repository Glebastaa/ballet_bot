import os

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from database.models import UserRoles
from exceptions import SameRoleError, UserAlreadyExistsError
from utils.states import AdminPass, RegUser
from services.user import UserService
from keyboards import inline


load_dotenv()

router = Router()
user_service = UserService()
ADMIN_PASS = os.getenv('ADMIN_PASS')


@router.message(RegUser.name)
async def set_username(message: Message, state: FSMContext):
    "Check username and add user"
    username = message.text
    curr_id = message.from_user.id

    try:
        new_user = await user_service.register_user(
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


@router.message(AdminPass.password)
async def check_admin_pass(message: Message, state: FSMContext):
    "Password verification and login to the admin panel"
    password = message.text
    if password == ADMIN_PASS:
        curr_id = message.from_user.id
        role = UserRoles.OWNER
        await user_service.switch_to_another_role(
            telegram_id=curr_id, role=role
        )
        await message.answer(
            'Вы вошли в панель администратора. Выберите действие',
            reply_markup=inline.show_admin_menu_kb()
        )
    else:
        await message.answer('Неверный пароль, попробуйте еще раз')
    await state.clear()


@router.message(AdminPass.switch_role)
async def switch_role(message: Message, state: FSMContext):
    "Changing the user's role by username"
    username = message.text
    user = await user_service.get_user_id_by_username(username)
    if user is None:
        await message.answer(
            f'Пользователь {username} не найден.'
        )
        await state.clear()
    else:
        try:
            curr_id = await user_service.get_user_id_by_username(username)
            data = await state.get_data()
            switch_role: UserRoles = data.get('switch_role')
            await user_service.switch_to_another_role(
                telegram_id=curr_id, role=switch_role
            )
            await message.answer(
                f'Роль для {username} изменена на {switch_role.value}'
            )
            await message.answer(
                'Выберите действие',
                reply_markup=inline.show_admin_menu_kb()
            )
            await state.clear()
        except SameRoleError:
            await message.answer(
                f'Роль для {username} уже изменена на {switch_role.value}'
            )
            await state.clear()
