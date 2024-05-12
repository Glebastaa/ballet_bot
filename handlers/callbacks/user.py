from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models import UserRoles
from services.user import UserService
from keyboards import inline, builders
from utils.states import AdminPass


router = Router()
user_service = UserService()


@router.callback_query(F.data.startswith('changeRole'))
async def change_role(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=await builders.switch_to_role_kb(
            'switchRole', user_name=None, user_id=None
        )
    )


@router.callback_query(F.data.startswith('switchRole'))
async def switch_role(callback: CallbackQuery, state: FSMContext):
    role = UserRoles(callback.data.split('_')[1])

    await state.update_data(role=role)
    await state.set_state(AdminPass.switch_role)
    await callback.message.edit_text(
        'Введите логин пользователя для измения роли'
    )
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('showUsersRole'))
async def step1_show_role(callback: CallbackQuery):
    await callback.message.edit_reply_markup(
        reply_markup=inline.show_users_role_kb()
    )


@router.callback_query(F.data.startswith('showRole'))
async def step2_show_role(callback: CallbackQuery):
    role = callback.data.split('_')[1]
    if role == 'owner':
        role = UserRoles.OWNER
    elif role == 'teacher':
        role = UserRoles.TEACHER
    else:
        role = UserRoles.STUDENT
    users = await user_service.get_users_by_role(role)
    kb = await builders.show_users_for_role(users, role)
    await callback.message.edit_text(
        f'Список всех, кто имеет роль: {role.value}'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('allUsersForRole'))
async def show_user_menu(callback: CallbackQuery):
    username = callback.data.split('_')[1]
    curr_id = callback.data.split('_')[2]
    user = await user_service.get_user_by_id(telegram_id=curr_id)
    kb = inline.show_user_menu_kb(user_name=username, user_id=curr_id)
    await callback.message.edit_text(
        f'Выбранный пользователь: {username} с ролью {user.role.value}. '
        'Выберите действие:'
    )
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('switchRole'))
async def change_role_to_user(callback: CallbackQuery):
    username = callback.data.split('_')[1]
    curr_id = callback.data.split('_')[2]
    kb = await builders.switch_to_role_kb(
        'editRole', user_name=username, user_id=curr_id
    )
    await callback.message.edit_text(f'Выберите новую роль для {username}')
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith('editRole'))
async def edit_role_to_user(callback: CallbackQuery):
    role = UserRoles(callback.data.split('_')[1])
    username = callback.data.split('_')[2]
    curr_id = callback.data.split('_')[3]
    await user_service.switch_to_another_role(telegram_id=curr_id, role=role)
    await callback.message.edit_text(
        f'Роль для пользователя {username} изменена на {role.value}'
    )
    await callback.message.edit_reply_markup(reply_markup=None)
