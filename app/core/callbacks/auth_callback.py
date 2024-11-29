from pyrogram import enums

from app.core.keyboards.auth_keyboard import denied_keyboard
from app.enums.auth import RegistrationStates
from app.settings.config_settings import user_state


async def registration_callback(client, callback_query):
    user_id = callback_query.from_user.id
    user_state.set_state(user_id, RegistrationStates.WAITING_FOR_NAME)
    await callback_query.message.reply(
        "Введите <b>Ваше имя</b> ✍️\n\n"
        "Пример: <i>Иван</i> ",
        parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
    )


async def login_callback(client, callback_query):
    await callback_query.message.reply("Вы нажали Войти")
