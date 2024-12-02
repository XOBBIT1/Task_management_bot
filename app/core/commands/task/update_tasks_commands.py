from pyrogram import enums

from app.core.keyboards.auth_keyboard import auth_keyboard
from app.core.keyboards.task_keyboard import update_task_keyboard
from app.core.repositories.tasks import TasksRepository
from app.core.repositories.users import UsersRepository
from app.enums.tasks import UserTasksStates
from app.settings.config_settings import user_state, task_update


async def update_task_command(client, message):
    user = await UsersRepository().user_is_verified(chat_id=message.chat.id)
    task = await TasksRepository().get_task_by_id(task_id=int(task_update["task_id"]))
    if user:
        await message.reply(
            "<b>Выбирите, что вы хотите изменть!</b> ✍️\n\n"
            f"<b><i>Название: {task.task_name}</i></b>\n"
            f"<i>Описсание: {task.task_descriptions}</i>\n"
            f"<b><i>Статус: {task.readable_status}</i></b>\n"
            f"<b><i>Преоритет: {task.readable_priority}</i></b>\n",
            parse_mode=enums.ParseMode.HTML, reply_markup=update_task_keyboard(task.id)
        )
    else:
        await message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def task_update_name_command(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == UserTasksStates.WAITING_FOR_TASK_UPDATE_NAME:
        task_name = message.text
        task_update["task_name"] = task_name
        updated_task = await TasksRepository().update_task(
            task_id=task_update["task_id"],
            task_update_data=task_update
        )
        if updated_task:
            await message.reply(
                f"<b>Задача {task_name} обновлена!</b>✅\n\n",
                parse_mode=enums.ParseMode.HTML
            )
            await update_task_command(client, message)


async def task_update_description_command(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    task_name = task_update["task_name"]

    if state == UserTasksStates.WAITING_FOR_TASK_UPDATE_DESCRIPTION:
        task_descriptions = message.text
        task_update["task_descriptions"] = task_descriptions
        updated_task = await TasksRepository().update_task(
            task_id=task_update["task_id"],
            task_update_data=task_update
        )
        if updated_task:
            await message.reply(
                f"<b>Задача {task_name} обновлена!</b>✅\n\n",
                parse_mode=enums.ParseMode.HTML
            )
            await update_task_command(client, message)
