from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bots.middlewares import registered_user_required
from bots.middlewares.decorator import roles_user_required
from bots.keyboards import reply, inline
from services.user import UserService
from utils.states import RegUser, AdminPass


router = Router()
user_service = UserService()


@router.message(Command('start'))
async def start_main(message: Message, state: FSMContext):
    curr_id = message.from_user.id

    check_id = await user_service.get_user_by_id(telegram_id=curr_id)
    if check_id is None:
        await message.answer('Придумайте ваш никнейм (позже он понадобится)')
        await state.set_state(RegUser.wait_for_name)
    else:
        await message.answer(
            'Вы уже зарегестрированны! Используйте меню для работы с ботом'
        )


@router.message(Command('add'))
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def add_main(message: Message):
    await message.answer(
        'Выебирте, что вы хотите добавить:', reply_markup=reply.main
    )


@router.message(Command('show'))
@registered_user_required
@roles_user_required(['owner', 'teacher', 'student'])
async def show_main(message: Message):
    await message.answer(
        'Выебирте, что вы хотите увидеть:', reply_markup=reply.main_info
    )


@router.message(Command('delete'))
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def delete_main(message: Message):
    await message.answer(
        'Выебирте, что вы хотите удалить:', reply_markup=reply.main_delete
    )


@router.message(Command('edit'))
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def edit_main(message: Message):
    await message.answer(
        'Выебирте, что вы хотите изменить:', reply_markup=reply.main_edit
    )


@router.message(Command('admin'))
@registered_user_required
async def admin_board(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await user_service.get_user_by_id(telegram_id=user_id)
    if user.role.value != 'owner':
        await state.set_state(AdminPass.wait_for_pass)
        await message.answer('Введите пароль администратора:')
    else:
        await message.answer(
            'Вы вошли в панель администратора. Выберите действие',
            reply_markup=inline.show_admin_menu_kb()
        )


@router.message()
@registered_user_required
async def echo(message: Message):
    msg = message.text.lower()

    if msg == 'add':
        await message.answer(
            'Выебирте, что вы хотите добавить:', reply_markup=reply.main
        )
    elif msg == 'show':
        await message.answer(
            'Выебирте, что вы хотите увидеть:', reply_markup=reply.main_info
        )
    elif msg == 'delete':
        await message.answer(
            'Выебирте, что вы хотите удалить:', reply_markup=reply.main_delete
        )
    elif msg == 'edit':
        await message.answer(
            'Выебирте, что вы хотите изменить:', reply_markup=reply.main_edit
        )
    else:
        await message.answer(
            'Я не понимаю, что вы пишете. '
            'Для работы с ботом нажмите "Меню" и выберите, то, что вам надо'
        )
