import telebot
from telebot import types
from database import (add_group, add_studio, date_time_group, delete_group,
                      delete_studio, edit_group, edit_studio, get_groups,
                      get_studios)

bot = telebot.TeleBot("6583734890:AAE-oqtRv8oVkbW2ihUl7ClO_mHoQPyArhc")


# Общая функция для создания клавиатуры и отправки сообщения со списком студий
def send_studio_list(chat_id, studios):
    if studios:
        keyboard = types.InlineKeyboardMarkup()
        for studio_name in studios:
            btn_studio = types.InlineKeyboardButton(
                text=studio_name,
                callback_data=f'studio_{studio_name}'
            )
            keyboard.add(btn_studio)
        bot.send_message(chat_id, "Выберите студию:", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "В базе данных нет ни одной студии.")


# Добавление студии
@bot.message_handler(commands=['add_studio'])
def add_studio_command(message):
    bot.send_message(message.chat.id, "Введите название студии:")
    bot.register_next_step_handler(message, process_studio_name)


# Обработчик нажатия на кнопку "Добавить студию"
def process_studio_name(message):
    studio_name = message.text
    add_studio(studio_name)
    keyboard = types.InlineKeyboardMarkup()
    btn_studios = types.InlineKeyboardButton(
        text='Список студий',
        callback_data='list_studios'
    )
    keyboard.add(btn_studios)
    bot.send_message(message.chat.id,
                     f'Студия {studio_name} добавлена', reply_markup=keyboard)


# Удаление студии
@bot.message_handler(commands=['delete_studio'])
def delete_studio_command(message):
    studios = get_studios()
    if studios:
        keyboard = types.InlineKeyboardMarkup()
        for studio_name in studios:
            btn_studio = types.InlineKeyboardButton(
                text=studio_name,
                callback_data=f'delete_studio_{studio_name}'
            )
            keyboard.add(btn_studio)
        bot.send_message(
            message.chat.id,
            "Выберите студию для удаления:",
            reply_markup=keyboard
        )
    else:
        bot.send_message(message.chat.id, "В базе данных нет ни одной студии.")


# Показ списка студий
@bot.message_handler(commands=['show_studios'])
def show_studios_command(message):
    studios = get_studios()
    send_studio_list(message.chat.id, studios)


# Обработчик нажатия на кнопку "Список студий"
@bot.callback_query_handler(func=lambda call: call.data == 'list_studios')
def list_studios(callback_query):
    studios = get_studios()
    send_studio_list(callback_query.message.chat.id, studios)


# Обработчик нажатия на студию
@bot.callback_query_handler(func=lambda call: call.data.startswith('studio_'))
def handle_studio(callback_query):
    studio_name = callback_query.data.split('_')[1]
    keyboard = types.InlineKeyboardMarkup()
    btn_edit = types.InlineKeyboardButton(
        text='Изменить название', callback_data=f'edit_studio_{studio_name}'
    )
    btn_delete = types.InlineKeyboardButton(
        text='Удалить', callback_data=f'delete_studio_{studio_name}'
    )
    btn_group_list = types.InlineKeyboardButton(
        text='Список групп', callback_data=f'group_list_{studio_name}'
    )
    btn_add_group = types.InlineKeyboardButton(
        text='Добавить группу', callback_data=f'add_group_studio_{studio_name}'
    )
    keyboard.add(btn_edit)
    keyboard.add(btn_delete)
    keyboard.add(btn_group_list)
    keyboard.add(btn_add_group)
    bot.send_message(callback_query.message.chat.id,
                     f'Вы выбрали студию {studio_name}', reply_markup=keyboard)


# Обработчик для кнопки "Изменить" студии
@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_studio_'))
def handle_edit(callback_query):
    studio_name = callback_query.data.split('_')[2]
    bot.send_message(callback_query.message.chat.id,
                     f'Введите новое имя для студии {studio_name}:')
    bot.register_next_step_handler(
        callback_query.message,
        process_new_studio_name,
        studio_name
    )


def process_new_studio_name(message, studio_name):
    new_studio_name = message.text.strip()
    edit_studio_name = edit_studio(studio_name, new_studio_name)
    bot.send_message(message.chat.id,
                     f'Студия {studio_name} изменена на {edit_studio_name}')


# Обработчик для кнопки "Удалить" студии
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_studio_'))
def handle_delete(callback_query):
    studio_name = callback_query.data.split('_')[2]
    delete_studio(studio_name)
    bot.send_message(callback_query.message.chat.id,
                     f'Студия {studio_name} удалена')


# Обработчик для кнопки "Список групп" студии
@bot.callback_query_handler(func=lambda call: call.data.startswith('group_list_'))
def handle_group_list(callback_query):
    studio_name = callback_query.data.split('_')[2]
    groups = get_groups(studio_name)
    if groups:
        keyboard = types.InlineKeyboardMarkup()
        for group_name in groups:
            btn_group = types.InlineKeyboardButton(
                text=group_name,
                callback_data=f'group_{studio_name}_{group_name}'
            )
            keyboard.add(btn_group)
        bot.send_message(callback_query.message.chat.id,
                         f'Список групп для {studio_name}',
                         reply_markup=keyboard)
    else:
        bot.send_message(callback_query.message.chat.id,
                         f'В студии {studio_name} нет групп')


# Обработчик нажатия на кнопку "Добавить группу" студии
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_group_studio_'))
def handle_add_group_studio(callback_query):
    studio_name = callback_query.data.split('_')[3]
    bot.send_message(callback_query.message.chat.id,
                     f'Введите название группы для {studio_name}:')
    bot.register_next_step_handler(callback_query.message,
                                   process_group_name, studio_name)


"""Тута будет все про группы"""


# Добавление группы
@bot.message_handler(commands=['add_group'])
def add_group_command(message):
    bot.send_message(message.chat.id, "Введите название группы:")
    bot.register_next_step_handler(message, process_group_name)


# Обработчик ввода названия группы и выбора студии
def process_group_name(message, studio_name=None):
    group_name = message.text
    studios = get_studios()
    if studios:
        if studio_name:
            bot.send_message(message.chat.id, f"Введите день занятия для {group_name} в студии {studio_name} (в формате дня недели):")
            bot.register_next_step_handler(message, process_group_start_date,
                                           studio_name, group_name)
        else:
            keyboard = types.InlineKeyboardMarkup()
            for studio_name in studios:
                btn_studio = types.InlineKeyboardButton(
                    text=studio_name,
                    callback_data=f'add_group_{studio_name}_{group_name}'
                )
                keyboard.add(btn_studio)
            bot.send_message(message.chat.id,
                             f"Выберите студию для группы {group_name}:",
                             reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "В базе данных нет ни одной студии.")


# Обработчик нажатия на студию для добавления группы
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_group_'))
def handle_add_group(callback_query):
    studio_name = callback_query.data.split('_')[2]
    group_name = callback_query.data.split('_')[3]
    bot.send_message(
        callback_query.message.chat.id,
        f"Введите день занятия для {group_name} (в формате дня недели):"
    )
    bot.register_next_step_handler(callback_query.message,
                                   process_group_start_date,
                                   studio_name, group_name)


# Обработчик ввода дня начала занятия группы
def process_group_start_date(message, studio_name, group_name):
    start_date = message.text.strip()
    bot.send_message(message.chat.id, f"Введите время начала занятия для группы {group_name} (в формате '17:00'):")
    bot.register_next_step_handler(message, process_group_start_time,
                                   studio_name, group_name, start_date)


# Обработчик ввода времени начала занятия группы
def process_group_start_time(message, studio_name, group_name, start_date):
    start_time = message.text.strip()
    add_group(group_name, studio_name, start_time, start_date)
    bot.send_message(message.chat.id, f"Группа {group_name} добавлена к студии {studio_name} с началом занятия {start_date} в {start_time}")


# Обработчик нажатия на группу
@bot.callback_query_handler(func=lambda call: call.data.startswith('group_'))
def handle_group(callback_query):
    studio_name = callback_query.data.split('_')[1]
    group_name = callback_query.data.split('_')[2]
    group_data = date_time_group(group_name, studio_name)
    if group_data:
        start_date, start_time = group_data
        new_start_time = start_time.strftime('%H:%M')
    else:
        start_date, start_time = None, None
    keyboard = types.InlineKeyboardMarkup()
    btn_edit = types.InlineKeyboardButton(
        text='Изменить', callback_data=f'edit_group_{studio_name}_{group_name}'
    )
    btn_delete = types.InlineKeyboardButton(
        text='Удалить', callback_data=f'delete_group_{studio_name}_{group_name}'
    )
    keyboard.add(btn_edit, btn_delete)
    bot.send_message(callback_query.message.chat.id,
                     f'Группа: {group_name}\n'  # Имя группы
                     f'📅 День: {start_date} 📅\n'  # Дата
                     f'⏰ Время: {new_start_time} ⏰\n',  # Время
                     reply_markup=keyboard)


# Обработчик для кнопки "Изменить" группы
@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_group_'))
def handle_edit_group(callback_query):
    studio_name = callback_query.data.split('_')[2]
    group_name = callback_query.data.split('_')[3]
    bot.send_message(callback_query.message.chat.id,
                     f'Введите новое название группы {group_name}:')
    bot.register_next_step_handler(callback_query.message,
                                   process_new_group_name,
                                   group_name, studio_name)


def process_new_group_name(message, group_name, studio_name):
    new_group_name = message.text.strip()
    edit_group_name = edit_group(group_name, new_group_name, studio_name)
    bot.send_message(message.chat.id,
                     f'Группа {group_name} изменена на {edit_group_name}')


# Обработчик для кнопки "Удалить" группы
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_group_'))
def handle_delete_group(callback_query):
    group_name = callback_query.data.split('_')[3]
    studio_name = callback_query.data.split('_')[2]
    delete_group(group_name, studio_name)
    bot.send_message(callback_query.message.chat.id,
                     f'Группа {group_name} удалена')


bot.polling(none_stop=True)
