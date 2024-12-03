from pyrogram import Client
from pyrogram.types import Message

from app.core.commands.auth.login_commands import loging_get_email, loging_get_password
from app.core.commands.auth.registration_commands import registration_get_name, registration_get_email, \
    registration_get_password
from app.core.commands.task.create_task_commands import get_task_name_command, create_task_command
from app.core.commands.task.update_tasks_commands import task_update_description_command, task_update_name_command
from app.core.commands.user_commands import user_update_name, user_update_email
from app.enums.auth import RegistrationStates, LoginStates
from app.enums.tasks import UserTasksStates
from app.enums.user import UpdateUserStates
from app.settings.config_settings import user_state

commands_map = {
    RegistrationStates.WAITING_FOR_NAME: registration_get_name,
    RegistrationStates.WAITING_FOR_EMAIL: registration_get_email,
    RegistrationStates.WAITING_FOR_PASSWORD: registration_get_password,
    LoginStates.WAITING_FOR_LOGING_EMAIL: loging_get_email,
    LoginStates.WAITING_FOR_LOGING_PASSWORD: loging_get_password,
    UpdateUserStates.WAITING_FOR_UPDATE_NAME: user_update_name,
    UpdateUserStates.WAITING_FOR_UPDATE_EMAIL: user_update_email,
    UserTasksStates.WAITING_FOR_TASK_NAME: get_task_name_command,
    UserTasksStates.WAITING_FOR_TASK_DESCRIPTION: create_task_command,
    UserTasksStates.WAITING_FOR_TASK_UPDATE_NAME: task_update_name_command,
    UserTasksStates.WAITING_FOR_TASK_UPDATE_DESCRIPTION: task_update_description_command,
}


async def commands_manager(client: Client, message: Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    # Ищем соответствующую команду по состоянию
    command = commands_map.get(state)

    if command:
        await command(client, message)
    else:
        # Можно добавить обработку ошибки или возврат пользователю, если состояние не найдено
        await message.reply("Неизвестное состояние. Попробуйте позже.")
