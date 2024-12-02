from pyrogram import enums

from app.core.keyboards.auth_keyboard import auth_keyboard
from app.core.keyboards.task_keyboard import user_tasks_keyboard, all_tasks_keyboard
from app.core.repositories.tasks import TasksRepository
from app.core.repositories.users import UsersRepository


async def tasks_main_menu_callback(client, callback_query):
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


async def get_all_tasks_callback(client, callback_query):
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
