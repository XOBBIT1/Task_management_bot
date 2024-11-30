from pyrogram import enums

from app.core.commands.auth.registration_commands import start_command
from app.core.keyboards.auth_keyboard import denied_keyboard
from app.core.repositories.users import UsersRepository
from app.enums.auth import LoginStates
from app.settings.config_settings import user_state, user_login


async def try_again_login(client, message):
    user_id = message.from_user.id
    user_state.set_state(user_id, LoginStates.WAITING_FOR_LOGING_EMAIL)
    await message.reply(
        "Введите <b>Вашу почту</b> ✍️\n\n",
        parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
    )


async def loging_get_email(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == LoginStates.WAITING_FOR_LOGING_EMAIL:
        user_email = message.text
        user_login["email"] = user_email
        user_state.set_state(user_id, LoginStates.WAITING_FOR_LOGING_PASSWORD)

        await message.reply(
            "Введите пароль",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )


async def loging_get_password(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == LoginStates.WAITING_FOR_LOGING_PASSWORD:
        user_password = message.text
        user_login["password"] = user_password
        verified_user = await UsersRepository().verify_user(
            email=user_login.get("email"),
            password=user_login.get("password")
        )
        if verified_user:
            await message.reply(
                "<b>ДОБРО ПОЖАЛОВТЬ!</b>✅\n\n",
                parse_mode=enums.ParseMode.HTML
            )
            await start_command(client, message)
        else:
            await message.reply(
                "<b>Не правильные email или пароль</b>✅\n\n"
                "Повторите попытку!",
                parse_mode=enums.ParseMode.HTML
            )
            await try_again_login(client, message)
