from pyrogram import enums

from app.core.commands.auth.registration_commands import start_command
from app.core.repositories.users import UsersRepository


async def logout_callback(client, callback_query):
    await UsersRepository().user_logout(chat_id=callback_query.message.chat.id)
    await callback_query.message.reply(
        "<b>Вы успешно вышли из системы!</b>",
        parse_mode=enums.ParseMode.HTML,
    )
    await start_command(client, callback_query.message)
