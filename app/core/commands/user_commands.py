from pyrogram import enums, Client
from pyrogram.types import Message

from app.core.keyboards.auth_keyboard import auth_keyboard
from app.core.keyboards.user_keyboard import user_profile_keyboard
from app.core.repositories.users import UsersRepository
from app.enums.user import UpdateUserStates
from app.settings.config_settings import user_state, user_update


async def user_profile_command(client: Client, message: Message):
    """
    Отображает профиль пользователя с его текущими данными, такими как имя и email.
    Также предоставляет возможность обновить эти данные.

    Аргументы:
        client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
        message (Message): Сообщение от пользователя, вызвавшего команду.

    Отправляет:
        Сообщение с профилем пользователя и кнопками для изменения имени и почты.
        В случае неавторизованного пользователя отправляется сообщение с просьбой войти в систему.
    """
    user = await UsersRepository().user_is_verified(chat_id=message.chat.id)
    if user:
        await message.reply(
            "Это <b>Ваше профиль!</b> ✍️\n\n"
            f"Ваше имя: <b>{user.name}</b>\n"
            f"Ваша почта: <b>{user.email}</b>\n\n"
            "Здесь Вы можете поменять:\n"
            " 1. Своё имя 🫥\n"
            " 2. Свою почту 📩",
            parse_mode=enums.ParseMode.HTML, reply_markup=user_profile_keyboard()
        )
    else:
        await message.reply(
            "🔴\n\n"
            "<b>Вы не вошли в систему!</b>\n\n"
            "Для этого <b><i>зарегистрируйтесь или войдите</i></b> в <b>СИСТЕМУ</b>",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard())


async def user_update_name(client: Client, message: Message):
    """
   Обрабатывает команду для обновления имени пользователя. Сохраняет новое имя в базе данных.

   Аргументы:
       client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
       message (Message): Сообщение от пользователя, содержащее новое имя.

   Отправляет:
       Сообщение с подтверждением успешного обновления имени.
   """
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == UpdateUserStates.WAITING_FOR_UPDATE_NAME:
        user_name = message.text
        user_update["name"] = user_name
        updated_user = await UsersRepository().update_user(
            chat_id=message.chat.id,
            user_data=user_update
        )
        if updated_user:
            await message.reply(
                f"<b>Ваше новое ИМЯ: {user_name}</b>✅\n\n",
                parse_mode=enums.ParseMode.HTML
            )
            await user_profile_command(client, message)


async def user_update_email(client: Client, message: Message):
    """
    Обрабатывает команду для обновления почты пользователя. Сохраняет новый email в базе данных.

    Аргументы:
        client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
        message (Message): Сообщение от пользователя, содержащее новый email.

    Отправляет:
        Сообщение с подтверждением успешного обновления почты.
    """
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == UpdateUserStates.WAITING_FOR_UPDATE_EMAIL:
        user_email = message.text
        user_update["email"] = user_email
        updated_user = await UsersRepository().update_user(
            chat_id=message.chat.id,
            user_data=user_update
        )
        if updated_user:
            await message.reply(
                f"<b>Ваша новая Почта: {user_email}</b>✅\n\n",
                parse_mode=enums.ParseMode.HTML
            )
            await user_profile_command(client, message)
