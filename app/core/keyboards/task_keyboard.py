from pyrogram import types


def user_tasks_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Создать задачу 🖊", callback_data="create_task")],
        [types.InlineKeyboardButton(text="Изменить задачу ✍️", callback_data="change_task")],
        [types.InlineKeyboardButton(text="Мои задачи 📝", callback_data="my_tasks")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def all_tasks_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Изменить задачу ✍️", callback_data="change_task")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
