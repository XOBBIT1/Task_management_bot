from pyrogram import enums, Client, types

from app.core.keyboards.auth_keyboard import denied_keyboard, auth_keyboard
from app.core.keyboards.user_keyboard import user_profile_keyboard
from app.core.repositories.users import UsersRepository
from app.enums.user import UpdateUserStates
from app.settings.config_settings import user_state


async def user_profile_callback(client: Client, callback_query: types.CallbackQuery):
    """
   Обрабатывает callback-запрос для отображения профиля пользователя.

   Если пользователь авторизован, отправляет сообщение с информацией о профиле, включая имя и почту,
   а также предоставляет возможности для изменения этих данных. Если пользователь не авторизован,
   предлагает зарегистрироваться или войти в систему.

   Args:
       client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
       callback_query: Объект callback-запроса, инициированный пользователем.
   """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        await callback_query.message.reply(
            "Это <b>Ваше профиль!</b> ✍️\n\n"
            f"Ваше имя: <b>{user.name}</b>\n"
            f"Ваша почта: <b>{user.email}</b>\n\n"
            "Здесь Вы можете поменять:\n"
            " 1. Своё имя 🫥\n"
            " 2. Свою почту 📩",
            parse_mode=enums.ParseMode.HTML, reply_markup=user_profile_keyboard()
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def update_user_name_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает callback-запрос для изменения имени пользователя.

    Если пользователь авторизован, переводит его в состояние ожидания ввода нового имени
    и отправляет соответствующее сообщение. Если пользователь не авторизован, предлагает
    зарегистрироваться или войти в систему.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        user_id = callback_query.from_user.id
        user_state.set_state(user_id, UpdateUserStates.WAITING_FOR_UPDATE_NAME)
        await callback_query.message.reply(
            "Введите <b>Ваше НОВОЕ имя</b> ✍️\n\n"
            "Пример: <i>Иван</i> ",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def update_user_email_callback(client: Client, callback_query: types.CallbackQuery):
    """
   Обрабатывает callback-запрос для изменения почты пользователя.

   Если пользователь авторизован, переводит его в состояние ожидания ввода новой почты
   и отправляет соответствующее сообщение. Если пользователь не авторизован, предлагает
   зарегистрироваться или войти в систему.

   Args:
       client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
       callback_query: Объект callback-запроса, инициированный пользователем.
   """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        user_id = callback_query.from_user.id
        user_state.set_state(user_id, UpdateUserStates.WAITING_FOR_UPDATE_EMAIL)
        await callback_query.message.reply(
            "Введите <b>Вашу НОВУЮ почту</b> 📩\n\n"
            "Пример: <i>example@mail.com</i>",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())
