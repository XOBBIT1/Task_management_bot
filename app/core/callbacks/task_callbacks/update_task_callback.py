from pyrogram import enums, Client, types

from app.core.keyboards.auth_keyboard import auth_keyboard, denied_keyboard
from app.core.keyboards.task_keyboard import update_task_keyboard, update_task_status_keyboard, \
    update_task_priority_keyboard
from app.core.repositories.users import UsersRepository
from app.core.repositories.tasks import TasksRepository
from app.enums.tasks import UserTasksStates
from app.settings.config_settings import user_state, task_update


async def update_task_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает запрос на обновление задачи. Если пользователь авторизован, показывает меню с текущими данными
    задачи и возможностью выбрать, что именно нужно изменить (название, описание, статус, приоритет). Если
    пользователь не авторизован, предлагается зарегистрироваться или войти в систему.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    task_id = callback_query.data.split('_')[2]
    task_update["task_id"] = int(task_id)
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    task = await TasksRepository().get_task_by_id(task_id=int(task_id))
    task_update["task_name"] = task.task_name
    if user:
        await callback_query.message.reply(
            "<b>Выбирите, что вы хотите изменть:</b> ✍️\n\n"
            f"<b><i>Название: {task.task_name}</i></b>\n"
            f"<i>Описсание: {task.task_descriptions}</i>\n"
            f"<b><i>Статус: {task.readable_status}</i></b>\n"
            f"<b><i>Преоритет: {task.readable_priority}</i></b>\n",
            parse_mode=enums.ParseMode.HTML, reply_markup=update_task_keyboard(task_update["task_id"])
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def update_name_task_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает запрос на обновление названия задачи. Если пользователь авторизован, переводит его в состояние
    ожидания нового имени задачи. Если пользователь не авторизован, предлагается зарегистрироваться или войти в систему.

        Args:
            client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
            callback_query: Объект callback-запроса, инициированный пользователем.
        """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        user_id = callback_query.from_user.id
        user_state.set_state(user_id, UserTasksStates.WAITING_FOR_TASK_UPDATE_NAME)
        await callback_query.message.reply(
            "Введите <b>НОВОЕ название ЗАДАЧИ</b> ✍️\n\n"
            "Пример: <i>Исправленеи ошибок</i> ",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def update_desc_task_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает запрос на обновление описания задачи. Если пользователь авторизован, переводит его в состояние ожидания
    нового описания задачи. Если пользователь не авторизован, предлагается зарегистрироваться или войти в систему.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        user_id = callback_query.from_user.id
        user_state.set_state(user_id, UserTasksStates.WAITING_FOR_TASK_UPDATE_DESCRIPTION)
        await callback_query.message.reply(
            "Введите <b>НОВОЕ описание ЗАДАЧИ</b> ✍️\n\n"
            "Пример: <i>Исправить баг с вводом данных почты в регистрации.</i>",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def update_status_task_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает запрос на обновление статуса задачи. Если пользователь авторизован, показывает меню с возможными
    статусами для задачи. Если пользователь не авторизован, предлагается зарегистрироваться или войти в систему.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        await callback_query.message.reply(
            "<b>Выбирите статус из придложенных.</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=update_task_status_keyboard(task_update["task_id"])
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def update_priority_task_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает запрос на обновление приоритета задачи. Если пользователь авторизован, показывает меню с возможными
    приоритетами для задачи. Если пользователь не авторизован, предлагается зарегистрироваться или войти в систему.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    user = await UsersRepository().user_is_verified(chat_id=callback_query.message.chat.id)
    if user:
        await callback_query.message.reply(
            "<b>Выбирите преоритет из придложенных.</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=update_task_priority_keyboard(task_update["task_id"])
        )
    else:
        await callback_query.message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def update_status_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает обновление статуса задачи. После успешного обновления статус задачи сохраняется, и пользователю
    отправляется уведомление о завершении обновления.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    status = callback_query.data.split('_')[1]
    task_update["status"] = status
    task_name = task_update["task_name"]
    updated_task = await TasksRepository().update_task(
        task_id=task_update["task_id"],
        task_update_data=task_update
    )
    if updated_task:
        await callback_query.message.reply(
            f"<b>Задача {task_name} обновлена!</b>✅\n\n",
            parse_mode=enums.ParseMode.HTML
        )
        await update_task_callback(client, callback_query)


async def update_priority_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает обновление приоритета задачи. После успешного обновления приоритет задачи сохраняется, и пользователю отправляется
    уведомление о завершении обновления.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    priority = callback_query.data.split('_')[1]
    task_update["priority"] = priority
    task_name = task_update["task_name"]
    updated_task = await TasksRepository().update_task(
        task_id=task_update["task_id"],
        task_update_data=task_update
    )
    if updated_task:
        await callback_query.message.reply(
            f"<b>Задача {task_name} обновлена!</b>✅\n\n",
            parse_mode=enums.ParseMode.HTML
        )
        await update_task_callback(client, callback_query)
