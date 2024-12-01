from pyrogram import types


def user_profile_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Изменить имя 🫥", callback_data="change_name")],
        [types.InlineKeyboardButton(text="Изменить почту 📩", callback_data="change_email")],
        [types.InlineKeyboardButton(text="Выход 🔜", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
