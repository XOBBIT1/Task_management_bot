from pyrogram import types


def back_keyboard():

    buttons = [
        [types.InlineKeyboardButton(text="Вернуться к предыдущему меню 🔙", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
