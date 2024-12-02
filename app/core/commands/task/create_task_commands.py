from pyrogram import enums

from app.core.keyboards.auth_keyboard import denied_keyboard, auth_keyboard
from app.core.keyboards.task_keyboard import user_tasks_keyboard
from app.core.repositories.tasks import TasksRepository
from app.core.repositories.users import UsersRepository
from app.enums.tasks import UserTasksStates
from app.settings.config_settings import create_task, user_state


async def tasks_main_menu_command(client, message):
    user = await UsersRepository().user_is_verified(chat_id=message.chat.id)
    if user:
        await message.reply(
            "<b>Меню ЗАДАЧ 📋</b>\n\n"
            "Здесь Вы можете:\n"
            "🖋🖌🖍 <i>Создавать и управлять задачами.\n</i>"
            "📊 <i>Отслеживайть прогресс выполнения задач.\n</i>",
            parse_mode=enums.ParseMode.HTML, reply_markup=user_tasks_keyboard()
        )
    else:
        await message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def get_task_name_command(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == UserTasksStates.WAITING_FOR_TASK_NAME:
        task_name = message.text
        create_task["task_name"] = task_name
        user_state.set_state(user_id, UserTasksStates.WAITING_FOR_TASK_DESCRIPTION)

        await message.reply(
            "<b>Напишите описание задачи.</b>\n\n"
            "Пример: <i>Исправить баг с вводом данных почты в регистрации.</i>",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )


async def create_task_command(client, message):
    user = await UsersRepository().user_is_verified(chat_id=message.chat.id)
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == UserTasksStates.WAITING_FOR_TASK_DESCRIPTION:
        task_descriptions = message.text
        create_task["task_descriptions"] = task_descriptions
        task = await TasksRepository().create_task(instance=create_task, creator_id=user.id)
        await message.reply(
            f"Задача {task.task_name} успешно создана! ✅",
            parse_mode=enums.ParseMode.HTML
        )
    await tasks_main_menu_command(client, message)
