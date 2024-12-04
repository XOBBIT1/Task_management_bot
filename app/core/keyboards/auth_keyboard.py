from pyrogram import types


def auth_keyboard():
    """
    Создает клавиатуру с кнопками для регистрации и входа.

    Возвращает:
        types.InlineKeyboardMarkup: Клавиатура с двумя кнопками:
            - Регистрация
            - Вход
    """
    buttons = [
        [types.InlineKeyboardButton(text="Регистрация 🧑‍💻", callback_data="registration")],
        [types.InlineKeyboardButton(text="Вход 🔜", callback_data="login")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def denied_keyboard():
    """
   Создает клавиатуру с кнопкой для отмены действия.

   Возвращает:
       types.InlineKeyboardMarkup: Клавиатура с одной кнопкой "Отменить".
   """
    buttons = [
        [types.InlineKeyboardButton(text="❌Отменить❌", callback_data="denied")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def loging_keyboard():
    """
    Создает клавиатуру с кнопкой для входа в систему.

    Возвращает:
        types.InlineKeyboardMarkup: Клавиатура с кнопкой "Вход".
    """
    buttons = [
        [types.InlineKeyboardButton(text="Вход 🔜", callback_data="login")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def main_menu_keyboard():
    """
    Создает клавиатуру с кнопками для основного меню пользователя.

    Возвращает:
        types.InlineKeyboardMarkup: Клавиатура с кнопками:
            - Мой профиль
            - Управление задачами
            - Выход из системы
    """
    buttons = [
        [types.InlineKeyboardButton(text="Мой профиль 🧑🫥", callback_data="my_profile")],
        [types.InlineKeyboardButton(text="Управление задачами. 📝💻", callback_data="tasks_management")],
        [types.InlineKeyboardButton(text="🚫Выход изи системы🚫", callback_data="logout")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
