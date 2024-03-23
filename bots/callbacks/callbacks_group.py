from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from exceptions import StudentAlreadyInGroupError
from bots.keyboards import inline, builders
from services.group import GroupService
from services.student import StudentService
from utils.states import EditGroup
from bots.callbacks.callbacks_studio import extract_data_from_callback

router = Router()

group_service = GroupService()
student_service = StudentService()


async def group_callback(
        callback: CallbackQuery,
        action: str,
        state: FSMContext = None  # type: ignore
) -> None:
    """Manage callback requests related to groups."""
    group_name, group_id = extract_data_from_callback(callback)
    message = callback.message

    if action == 'pick_group':
        studio_name = callback.data.split('_')[4]
        studio_id: int = callback.data.split('_')[5]  # type: ignore
        keyboard = inline.select_group_for_studio_kb(
            group_name, group_id, studio_name, studio_id
        )
        await message.edit_text(f'Выбрана группа {group_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'delete_group':
        await group_service.delete_group(group_id)
        await message.answer(f'Группа {group_name} успешно удалена')

    elif action == 'edit_group':
        studio_name = callback.data.split('_')[4]
        await state.update_data(group_name=group_name, group_id=group_id)
        await state.set_state(EditGroup.new_group_name)
        await message.edit_text(
            f'Студия: {studio_name}\nВведите новое имя для группы {group_name}'
        )
        await message.edit_reply_markup(reply_markup=None)

    elif action == 'add_shedule':
        studio_id: int = int(callback.data.split('_')[4])
        studio_name: str = callback.data.split('_')[5]
        await state.update_data(
            group_name=group_name,
            group_id=group_id,
            studio_id=studio_id,
            studio_name=studio_name
        )
        await message.edit_text(
            f'Выберите день занятия для группы {group_name}'
        )
        await message.edit_reply_markup(
            reply_markup=await builders.process_select_weekdays(
                action='group'  # type: ignore
            )
        )

    elif action == 'add_student':
        keyboard = await builders.show_list_students_menu(
            action='add_student2'
        )
        await state.update_data(group_name=group_name, group_id=group_id)
        await message.edit_text(
            f'Выберите ученика для добавления его в группу {group_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'list_students':
        keyboard = await builders.show_list_students_from_group_menu(
            'pick_student', group_id
        )
        keyboard2 = await builders.show_list_studios_menu('list_group')
        students = await student_service.get_students_from_group(group_id)

        if not students:
            await message.edit_text(
                f'Учеников нет в группе {group_name}. Выберите другую группу'
            )
            await message.edit_reply_markup(reply_markup=keyboard2)
            return

        await message.edit_text(f'Список учеников для группы {group_name}')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'delete_student':
        keyboard = await builders.show_list_students_from_group_menu(
            'delete_students', group_id
        )
        await state.update_data(group_name=group_name, group_id=group_id)
        await message.edit_text(
            f'Выберите ученика для удаления его из группы {group_name}'
        )
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'pick_groups':
        #  student_name: str = callback.data.split('_')[4]
        #  student_id: int = int(callback.data.split('_')[5])
        keyboard = inline.select_student_for_group_kb(group_name, group_id)
        await message.edit_text('Выбери сцука')
        await message.edit_reply_markup(reply_markup=keyboard)

    elif action == 'add_student3':
        data = await state.get_data()
        studio_name = data.get('studio_name', '1')
        studio_id: int = data.get('studio_id', 1)
        student_name = data.get('student_name')
        student_id: int = data.get('student_id', 1)
        keyboard = await builders.show_list_groups_menu(
            action='add_student3',
            studio_name=studio_name,
            studio_id=studio_id
        )

        try:
            await student_service.add_student_to_group(
                student_id=student_id,
                group_id=group_id,
                is_individual=False
            )
            await message.edit_text(
                f'Ученик {student_name} добавлен в группу {group_name}'
            )
            await message.edit_reply_markup(reply_markup=None)
            await state.clear()

        except StudentAlreadyInGroupError:
            await message.answer(
                f'Ученик {student_name} уже находится в {group_name}. '
                f'Выберите другую группу:',
                reply_markup=keyboard
            )

    elif action == 'delete_indiv':
        await group_service.delete_group(group_id)
        await message.answer(f'Индив {group_name} успешно удалена')
        await message.edit_reply_markup(reply_markup=None)


# Выбор группы и взаимодействие с ней
@router.callback_query(F.data.startswith('pick_group_'))
async def select_group_for_studio(callback: CallbackQuery) -> None:
    await group_callback(callback, 'pick_group')


@router.callback_query(F.data.startswith('delete_group_'))
async def call_delete_group(callback: CallbackQuery) -> None:
    await group_callback(callback, 'delete_group')


# Изменение имени группы и передача на шаг new_group_name
@router.callback_query(F.data.startswith('edit_group_'))
async def call_edit_group(callback: CallbackQuery, state: FSMContext) -> None:
    await group_callback(callback, 'edit_group', state)


@router.callback_query(F.data.startswith('add_shedule_'))
async def call_add_shedule(callback: CallbackQuery, state: FSMContext) -> None:
    await group_callback(callback, 'add_shedule', state)


# Выбор ученика для добавления в группу
@router.callback_query(F.data.startswith('add_student_'))
async def call_add_student_to_group(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await group_callback(callback, 'add_student', state)


# Показ списка учеников для группы
@router.callback_query(F.data.startswith('list_students_'))
async def call_list_students(callback: CallbackQuery) -> None:
    await group_callback(callback, 'list_students')


# Удаление ученика из группы
@router.callback_query(F.data.startswith('delete_student_'))
async def call_delete_student_from_group(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await group_callback(callback, 'delete_student', state)


@router.callback_query(F.data.startswith('pick_groups_'))
async def call_pick_groups_for_student(callback: CallbackQuery) -> None:
    await group_callback(callback, 'pick_groups')


@router.callback_query(F.data.startswith('add_student3_'))
async def call_add_student_to_group_ty_main_menu(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await group_callback(callback, 'add_student3', state)


@router.callback_query(F.data.startswith('delete_indiv_'))
async def call_delete_indiv_from_studio(callback: CallbackQuery) -> None:
    await group_callback(callback, 'delete_indiv')
