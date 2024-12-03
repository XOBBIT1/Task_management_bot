from pyrogram import enums, Client, types

from app.core.callbacks.task_callbacks.main_menu_callback import tasks_main_menu_callback
from app.core.keyboards.auth_keyboard import auth_keyboard
from app.core.keyboards.task_keyboard import all_tasks_keyboard
from app.core.repositories.tasks import TasksRepository
from app.core.repositories.users import UsersRepository


async def get_all_tasks_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает callback-запрос для отображения всех задач пользователя.

    Если пользователь авторизован, извлекает список всех задач и отправляет их в виде сообщений.
    Если задач нет, уведомляет пользователя и перенаправляет его в главное меню задач. Если
    пользователь не авторизован, предлагает зарегистрироваться или войти в систему.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    tasks = await TasksRepository().get_all_tasks()
    if user:
        if tasks:
            await callback_query.message.reply(
                "<b>ВАШИ ЗАДАЧИ 📋: </b>\n\n", parse_mode=enums.ParseMode.HTML)
            for task in tasks:
                await callback_query.message.reply(
                    f"<b><i>Название: {task.task_name}</i></b>\n"
                    f"<i>Описсание: {task.task_descriptions}</i>\n"
                    f"<b><i>Статус: {task.readable_status}</i></b>\n"
                    f"<b><i>Преоритет: {task.readable_priority}</i></b>\n",
                    parse_mode=enums.ParseMode.HTML, reply_markup=all_tasks_keyboard(task.id)
                )
        else:
            await callback_query.message.reply(
                "<b>У вас пока нет задач 😥 </b>\n\n",
                parse_mode=enums.ParseMode.HTML)
            await tasks_main_menu_callback(client, callback_query)
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())
