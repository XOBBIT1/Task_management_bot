from pyrogram import enums, types, Client

from app.core.keyboards.auth_keyboard import denied_keyboard
from app.enums.auth import RegistrationStates, LoginStates
from app.settings.config_settings import user_state


async def registration_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает callback-запрос для начала процесса регистрации.

    Устанавливает состояние пользователя на ожидание ввода имени и отправляет сообщение с инструкциями
    по вводу имени. Включает клавиатуру с кнопкой "Отмена".

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user_id = callback_query.from_user.id
    user_state.set_state(user_id, RegistrationStates.WAITING_FOR_NAME)
    await callback_query.message.reply(
        "Введите <b>Ваше имя</b> ✍️\n\n"
        "Пример: <i>Иван</i> ",
        parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
    )


async def login_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает callback-запрос для начала процесса входа.

    Устанавливает состояние пользователя на ожидание ввода электронной почты и отправляет сообщение
    с инструкциями по вводу почты. Включает клавиатуру с кнопкой "Отмена".

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user_id = callback_query.from_user.id
    user_state.set_state(user_id, LoginStates.WAITING_FOR_LOGING_EMAIL)
    await callback_query.message.reply(
        "Введите <b>Вашу почту</b> ✍️\n\n",
        parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
    )
