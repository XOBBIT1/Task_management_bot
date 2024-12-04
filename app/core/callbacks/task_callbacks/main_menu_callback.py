from pyrogram import enums, Client, types

from app.core.keyboards.auth_keyboard import auth_keyboard
from app.core.keyboards.task_keyboard import user_tasks_keyboard
from app.core.repositories.users import UsersRepository


async def tasks_main_menu_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает callback-запрос для отображения главного меню задач.

    Если пользователь авторизован, отправляет сообщение с возможностями меню задач,
    включая создание и управление задачами, а также отслеживание прогресса. Если пользователь
    не авторизован, предлагает зарегистрироваться или войти в систему.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        await callback_query.message.reply(
            "<b>Меню ЗАДАЧ 📋</b>\n\n"
            "Здесь Вы можете:\n"
            "🖋🖌🖍 <i>Создавать и управлять задачами.\n</i>"
            "📊 <i>Отслеживайть прогресс выполнения задач.\n</i>",
            parse_mode=enums.ParseMode.HTML, reply_markup=user_tasks_keyboard()
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())
