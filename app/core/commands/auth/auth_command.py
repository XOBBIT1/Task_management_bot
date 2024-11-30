from app.core.commands.auth.login_commands import loging_get_email, loging_get_password
from app.core.commands.auth.registration_commands import registration_get_name, registration_get_email, \
    registration_get_password
from app.enums.auth import RegistrationStates, LoginStates
from app.settings.config_settings import user_state


async def start_auth(client, message):
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
