from pyrogram import types


def back_keyboard():
    """
    Создает клавиатуру с кнопкой для возврата к предыдущему меню.

    Возвращает:
        types.InlineKeyboardMarkup: Клавиатура с кнопкой "Вернуться к предыдущему меню".
    """
    buttons = [
        [types.InlineKeyboardButton(text="Вернуться к предыдущему меню 🔙", callback_data="back")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
