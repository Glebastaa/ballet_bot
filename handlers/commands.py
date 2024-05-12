from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import reply, inline
from services.user import UserService
from utils.states import AdminPass, RegUser
from middlewares.decorator import registered_user_required


router = Router()
user_service = UserService()


@router.message(Command('start'))
async def start_main(message: Message, state: FSMContext):
    curr_id = message.from_user.id
    user = await user_service.get_user_by_id(telegram_id=curr_id)
    if user is None:
        await message.answer('Придумайте ваш никнейм (позже он понадобится)')
        await state.set_state(RegUser.name)
    else:
        await message.answer(
            'Вы уже зарегестрированны! Используйте меню для работы с ботом\n'
            f'Ваш никнейм - {user.username}'
        )


@router.message(Command('main'))
@registered_user_required
async def add_main(message: Message):
    await message.answer('Выебирте 1 из вариантов:', reply_markup=reply.main)


@router.message(Command('admin'))
@registered_user_required
async def admin_board(message: Message, state: FSMContext):
    curr_id = message.from_user.id
    user = await user_service.get_user_by_id(telegram_id=curr_id)
    if user.role.value != 'owner':
        await state.set_state(AdminPass.password)
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

    if msg == 'main':
        await message.answer(
            'Выебирте 1 из вариантов:', reply_markup=reply.main
        )
    else:
        await message.answer(
            'Я не понимаю, что вы пишете. '
            'Для работы с ботом нажмите "Меню" и выберите, то, что вам надо'
        )
