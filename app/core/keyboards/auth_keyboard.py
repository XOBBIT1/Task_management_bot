from pyrogram import types


def auth_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Регистрация 🧑‍💻", callback_data="registration")],
        [types.InlineKeyboardButton(text="Вход 🔜", callback_data="login")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def denied_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="❌Отменить❌", callback_data="denied")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def loging_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Вход 🔜", callback_data="login")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Мой профиль 🧑🫥", callback_data="my_profile")],
        [types.InlineKeyboardButton(text="Управление задачами. 📝💻", callback_data="tasks_management")],
        [types.InlineKeyboardButton(text="🚫Выход изи системы🚫", callback_data="logout")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
