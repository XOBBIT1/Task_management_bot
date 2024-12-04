from pyrogram import enums, Client, types

from app.core.keyboards.auth_keyboard import denied_keyboard, auth_keyboard
from app.core.repositories.users import UsersRepository
from app.enums.tasks import UserTasksStates
from app.settings.config_settings import user_state


async def create_task_callback(client: Client, callback_query: types.CallbackQuery):
    """
   Обрабатывает callback-запрос для создания новой задачи.

   Если пользователь авторизован, переводит его в состояние ожидания ввода названия задачи
   и отправляет соответствующее сообщение с инструкцией. Если пользователь не авторизован,
   предлагает зарегистрироваться или войти в систему.

   Args:
       client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
       callback_query: Объект callback-запроса, инициированный пользователем.
   """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        user_id = callback_query.from_user.id
        user_state.set_state(user_id, UserTasksStates.WAITING_FOR_TASK_NAME)
        await callback_query.message.reply(
            "Введите <b>Название Задачи</b> ✍️\n\n"
            "Пример: <i>Исправленеи ошибок</i> ",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())
