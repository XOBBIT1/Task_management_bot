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


async def commands_manager(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    if state == RegistrationStates.WAITING_FOR_NAME:
        await registration_get_name(client, message)
    elif state == RegistrationStates.WAITING_FOR_EMAIL:
        await registration_get_email(client, message)
    elif state == RegistrationStates.WAITING_FOR_PASSWORD:
        await registration_get_password(client, message)
    elif state == LoginStates.WAITING_FOR_LOGING_EMAIL:
        await loging_get_email(client, message)
    elif state == LoginStates.WAITING_FOR_LOGING_PASSWORD:
        await loging_get_password(client, message)
    elif state == UpdateUserStates.WAITING_FOR_UPDATE_NAME:
        await user_update_name(client, message)
    elif state == UpdateUserStates.WAITING_FOR_UPDATE_EMAIL:
        await user_update_email(client, message)
    elif state == UserTasksStates.WAITING_FOR_TASK_NAME:
        await get_task_name_command(client, message)
    elif state == UserTasksStates.WAITING_FOR_TASK_DESCRIPTION:
        await create_task_command(client, message)
    elif state == UserTasksStates.WAITING_FOR_TASK_UPDATE_NAME:
        await task_update_name_command(client, message)
    elif state == UserTasksStates.WAITING_FOR_TASK_UPDATE_DESCRIPTION:
        await task_update_description_command(client, message)
