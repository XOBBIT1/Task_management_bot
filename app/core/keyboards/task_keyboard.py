from pyrogram import types


def user_tasks_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Создать задачу 🖊", callback_data="create_task")],
        [types.InlineKeyboardButton(text="Мои задачи 📝", callback_data="my_tasks")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def all_tasks_keyboard(task_id):
    buttons = [
        [types.InlineKeyboardButton(text="Изменить задачу ✍️", callback_data=f"change_task_{task_id}")],
        [types.InlineKeyboardButton(text="Удалить задачу ❌", callback_data=f"delete_task_{task_id}")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def update_task_keyboard(task_id):
    buttons = [
        [types.InlineKeyboardButton(text="✍️ Изменить название ✍️", callback_data="update_task_name")],
        [types.InlineKeyboardButton(text="📖 Изменить описание 📖", callback_data="update_task_desc")],
        [types.InlineKeyboardButton(text="🚥 Поменять статус 🚥", callback_data="update_task_status")],
        [types.InlineKeyboardButton(text="🔝 Поменять приоритет 🔝", callback_data="update_task_priority")],
        [types.InlineKeyboardButton(text="❌ Удалить задачу ❌", callback_data=f"delete_task_{task_id}")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def update_task_status_keyboard(task_id):
    buttons = [
        [types.InlineKeyboardButton(text="🔴 Новая 🔴", callback_data=f"status_NEW_{task_id}")],
        [types.InlineKeyboardButton(text="🟡 В процессе 🟡", callback_data=f"status_INPROGRESS_{task_id}")],
        [types.InlineKeyboardButton(text="🟢 Завершена 🟢", callback_data=f"status_COMPLETED_{task_id}")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def update_task_priority_keyboard(task_id):
    buttons = [
        [types.InlineKeyboardButton(text="Низкий", callback_data=f"priority_LOW_{task_id}")],
        [types.InlineKeyboardButton(text="Средний", callback_data=f"priority_MIDDLE_{task_id}")],
        [types.InlineKeyboardButton(text="Высокий", callback_data=f"priority_HIGH_{task_id}")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
