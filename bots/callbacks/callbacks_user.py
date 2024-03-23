from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.models import UserRoles
from services.user import UserService
from utils.states import AdminPass
from bots.keyboards import inline, builders


router = Router()


@router.callback_query(F.data.startswith('switch_role_'))
async def change_roll_owner_call(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """Handles callback for changing user's role."""
    switch_role = UserRoles(callback.data.split('_')[2])
    await state.update_data(switch_role=switch_role)
    await state.set_state(AdminPass.switch_role)
    await callback.message.edit_text(
        'Введите логин пользователя для измения роли'
    )
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('show_role_'))
async def show_role_call(callback: CallbackQuery) -> None:
    """Handles callback for displaying user's role."""
    check_role = callback.data.split('_')[2]
    if check_role == 'owner':
        role = UserRoles.OWNER
    elif check_role == 'teacher':
        role = UserRoles.TEACHER
    else:
        role = UserRoles.STUDENT
    users = await UserService().get_users_by_role(role=role)
    keyboard = await builders.show_users_for_role(users, check_role)
    await callback.message.edit_text(
        f'Список всех, кто имеет роль: {role.value}'
    )
    await callback.message.edit_reply_markup(
        reply_markup=keyboard  # type: ignore
    )


@router.callback_query(F.data.startswith('switch_to_role'))
async def change_role_kb(callback: CallbackQuery) -> None:
    """Handles callback for changing user's role using keyboard."""
    await callback.message.edit_reply_markup(
        reply_markup=await builders.switch_to_role_kb(
            action='switch_role', user_name=None, user_id=None,
        )  # type: ignore
    )


@router.callback_query(F.data.startswith('show_users_role'))
async def change_show_users_role(callback: CallbackQuery) -> None:
    """Handles callback for displaying user's roles."""
    await callback.message.edit_reply_markup(
        reply_markup=inline.show_users_role_kb()
    )


@router.callback_query(F.data.startswith('show_users_to_'))
async def show_user_menu_call(callback: CallbackQuery) -> None:
    """Handles callback for displaying user's menu."""
    user_name = callback.data.split('_')[3]
    user_id: int = int(callback.data.split('_')[4])
    user = await UserService().get_user_by_id(telegram_id=user_id)
    keyboard = inline.show_user_menu_kb(user_name=user_name, user_id=user_id)
    await callback.message.edit_text(
        f'Выбранный пользователь: {user_name} с ролью {user.role.value}. '
        'Что вы хотите сделать?'
    )
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data.startswith('change_role_'))
async def change_role_to_user_call(callback: CallbackQuery) -> None:
    """Handles callback for changing user's role."""
    user_name = callback.data.split('_')[2]
    user_id: int = int(callback.data.split('_')[3])
    keyboard = await builders.switch_to_role_kb(
        action='edit_role', user_name=user_name, user_id=user_id
    )
    await callback.message.edit_text(f'Выберите новую роль для {user_name}')
    await callback.message.edit_reply_markup(
        reply_markup=keyboard  # type: ignore
    )


@router.callback_query(F.data.startswith('edit_role_'))
async def edit_role_to_user_call(callback: CallbackQuery) -> None:
    """Handles callback for changing user's role."""
    role = UserRoles(callback.data.split('_')[2])
    user_name: str = callback.data.split('_')[3]
    user_id: int = int(callback.data.split('_')[4])
    await UserService().switch_to_another_role(telegram_id=user_id, role=role)
    await callback.message.edit_text(
        f'Роль для пользователя {user_name} изменена на {role.value}'
    )
    await callback.message.edit_reply_markup(reply_markup=None)
