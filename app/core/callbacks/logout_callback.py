from pyrogram import enums, Client, types

from app.core.commands.menu_commands import start_command
from app.core.repositories.users import UsersRepository


async def logout_callback(client: Client, callback_query: types.CallbackQuery):
    """
    Обрабатывает callback-запрос для выхода пользователя из системы.

    Выполняет действие выхода пользователя, удаляя информацию о сессии, и отправляет сообщение о
    успешном выходе. Затем перенаправляет пользователя на приветственное сообщение, вызывая
    функцию `start_command`.

    Args:
        client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
        callback_query: Объект callback-запроса, инициированный пользователем.
    """
    await UsersRepository().user_logout(chat_id=callback_query.message.chat.id)
    await callback_query.message.reply(
        "<b>Вы успешно вышли из системы!</b>",
        parse_mode=enums.ParseMode.HTML,
    )
    await start_command(client, callback_query.message)
