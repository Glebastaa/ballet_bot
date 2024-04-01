from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from services.student import StudentService
from bots.keyboards import builders
from utils.states import Studio, Group, Student
from bots.middlewares import registered_user_required
from bots.middlewares.decorator import roles_user_required

router = Router()

student_service = StudentService()


@router.message(F.text.lower() == 'добавить студию')
@registered_user_required
@roles_user_required(['owner'])
async def form_add_studio(message: Message, state: FSMContext):
    await state.set_state(Studio.name)
    await message.answer('Введите название студии:')


@router.message(F.text.lower() == 'список студий')
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def message_list_studios(message: Message):
    await message.answer(
        'Список студий:',
        reply_markup=await builders.show_list_studios_menu(
            action='pick_studio'
        )
    )


@router.message(F.text.lower() == 'удалить студию')
@registered_user_required
@roles_user_required(['owner'])
async def message_delete_studio(message: Message):
    await message.answer(
        'Выберите студию для удаления:',
        reply_markup=await builders.show_list_studios_menu(
            action='delete_studio'
        )
    )


@router.message(F.text.lower() == 'изменить имя студии')
@registered_user_required
@roles_user_required(['owner'])
async def form_change_name_studio(message: Message):
    await message.answer(
        'Выберите студию для изменения имени:',
        reply_markup=await builders.show_list_studios_menu(
            action='edit_studio'
        )
    )


@router.message(F.text.lower() == 'добавить группу')
@registered_user_required
@roles_user_required(['owner'])
async def form_add_group(message: Message, state: FSMContext):
    await message.answer(
        'Выберите студию, в которую хотите добавить группу',
        reply_markup=await builders.show_list_studios_menu(
            action='select_studio'
        )
    )


@router.message(F.text.lower() == 'удалить группу')
@registered_user_required
@roles_user_required(['owner'])
async def message_delete_group(message: Message):
    await message.answer(
        'Выберите студию в которой хотите удалить группу:',
        reply_markup=await builders.show_list_studios_menu(
            action='delete_groups'
        )
    )


@router.message(F.text.lower() == 'список групп')
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def message_list_groups(message: Message):
    await message.answer(
        'Выберите студию, в которой хотите просмотреть группы',
        reply_markup=await builders.show_list_studios_menu(action='list_group')
    )


@router.message(F.text.lower() == 'изменить имя группы')
@registered_user_required
@roles_user_required(['owner'])
async def form_change_name_group(message: Message):
    await message.answer(
        'Выберите студию, в которой хотите сменить название группы:',
        reply_markup=await builders.show_list_studios_menu(
            action='list_studios'
        )
    )


@router.message(F.text.lower() == 'добавить ученика')
@registered_user_required
@roles_user_required(['owner'])
async def form_add_student(message: Message, state: FSMContext):
    await state.set_state(Student.name)
    await message.answer('Введите имя ученика:')


@router.message(F.text.lower() == 'список учеников')
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def form_add_student_to_group(message: Message):
    await message.answer(
        'Список учеников:',
        reply_markup=await builders.show_list_students_menu(
            action='pick_student'
        )
    )


@router.message(Group.start_date, F.text)
async def start_date_wrong_input(message: Message):
    await message.reply(
        'Пожалуйста, используйте кнопки для выбора дня занятия'
    )
    await message.answer(
        'Выберите день занятия',
        reply_markup=await builders.process_select_weekdays(action='group')
    )


@router.message(F.text.lower() == 'добавить индив')
@registered_user_required
@roles_user_required(['owner'])
async def form_add_indiv(message: Message):
    await message.answer(
        'Выберите студию, в которой хотите добавить индивидуальный занятие',
        reply_markup=await builders.show_list_studios_menu(action='add_indiv')
    )


@router.message(F.text.lower() == 'удалить индив')
@registered_user_required
@roles_user_required(['owner'])
async def form_delete_indiv(message: Message):
    await message.answer(
        'Выберите студию, в которой хотите удалить индивидуальный занятие',
        reply_markup=await builders.show_list_studios_menu(
            action='select_studios'
        )
    )


@router.message(F.text.lower() == 'добавить ученика в группу')
@registered_user_required
@roles_user_required(['owner', 'teacher'])
async def form_add_student_from_group(message: Message):
    await message.answer(
        'Выберите ученика, которого хотите добавить',
        reply_markup=await builders.show_list_students_menu(
            action='select_student'
        )
    )


@router.message(F.text.lower() == 'удалить ученика')
@registered_user_required
@roles_user_required(['owner'])
async def form_delete_student(message: Message):
    students = await student_service.get_all_students()
    if students:
        await message.answer(
            'Выберите ученика, которого хотите удалить из базы данных',
            reply_markup=await builders.show_list_students_menu(
                action='fulldelete_student'
            )
        )
    else:
        await message.answer('В базе данных нет ни одного ученика')


@router.message(F.text.lower() == 'изменить имя ученика')
@registered_user_required
@roles_user_required(['owner'])
async def form_change_name_student(message: Message):
    students = await student_service.get_all_students()
    if students:
        await message.answer(
            'Выберите ученика, у которого, хотите изменить имя',
            reply_markup=await builders.show_list_students_menu(
                action='edit_student'
            ))
    else:
        await message.answer('В базе данных нет ни одного ученика')
