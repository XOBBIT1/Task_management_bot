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
        [types.InlineKeyboardButton(text="❌Отменить регистрацию❌", callback_data="denied")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Вход 🔜", callback_data="login")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
