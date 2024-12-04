import logging

from pyrogram import enums, Client
from pyrogram.types import Message

from app.core.commands.menu_commands import main_menu_command
from app.core.keyboards.auth_keyboard import denied_keyboard
from app.core.repositories.users import UsersRepository
from app.settings.email_validator import validate_user_email
from app.enums.auth import RegistrationStates
from app.settings.config_settings import user_state, user_registration


async def try_again_registration_email(client: Client, message: Message):
    """
   Обрабатывает повторный запрос на ввод электронной почты при регистрации.
   Устанавливает состояние пользователя в ожидание ввода почты и отправляет сообщение с запросом почты.

   Аргументы:
       client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
       message (Message): Сообщение пользователя, которое содержит команду для повторного ввода данных.

   Отправляет:
       Сообщение с запросом на ввод электронной почты пользователя.
   """
    user_id = message.from_user.id
    user_state.set_state(user_id, RegistrationStates.WAITING_FOR_EMAIL)
    await message.reply(
        "Введите <b>Вашу почту</b> ✍️\n\n"
        "Пример: <i>example@mail.com</i>",
        parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
    )


async def registration_get_name(client: Client, message: Message):
    """
    Обрабатывает ввод имени пользователя при регистрации.
    Сохраняет имя и ID чата в данных регистрации и запрашивает почту.

    Аргументы:
        client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
        message (Message): Сообщение пользователя, содержащее имя.

    Отправляет:
        Сообщение с запросом на ввод электронной почты пользователя.
    """
    user_registration["username"] = message.from_user.username
    user_registration["chat_id"] = message.chat.id
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == RegistrationStates.WAITING_FOR_NAME:
        name = message.text
        user_registration["name"] = name
        user_state.set_state(user_id, RegistrationStates.WAITING_FOR_EMAIL)

        await message.reply(
            "Теперь введите вашу почту 🧑📩\n\n"
            "Пример: <i>example@mail.com</i>",
            parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
        )


async def registration_get_email(client: Client, message: Message):
    """
   Обрабатывает ввод электронной почты пользователя при регистрации.
   Проверяет формат почты и наличие пользователя с таким адресом. Если почта валидна, запрашивает пароль.

   Аргументы:
       client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
       message (Message): Сообщение пользователя, содержащее электронную почту.

   Отправляет:
       Сообщение с запросом на ввод пароля или уведомление о неправильном формате почты.
   """
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == RegistrationStates.WAITING_FOR_EMAIL:
        user_email = message.text
        user_registration["email"] = user_email
        if not await validate_user_email(user_email):
            await message.reply("Некорректный формат почты 📩. Попробуйте снова.")
            await try_again_registration_email(client, message)
        else:
            user = await UsersRepository().get_user_by_email(email=user_email)
            if user:
                logging.warning(f"Duplicate email attempt: {user_email} by user {message.from_user.id}")
                await message.reply(
                    "Пользовтель с такой почтой уже существует!\n\n"
                    "<b>Напишите другую почту</b>",
                    parse_mode=enums.ParseMode.HTML
                )
                await try_again_registration_email(client, message)
                raise Exception("User with such email already exists")
            else:
                user_state.set_state(user_id, RegistrationStates.WAITING_FOR_PASSWORD)
                await message.reply(
                    "Отлично осталось только придумать пароль!\n"
                    "<b>НИКОМУ НЕ СООБЩАЙТЕ ЕГО 🤫</b>\n\n"
                    "Пример: <i>AWD-dwdw212_1_@</i>",
                    parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
                )


async def registration_get_password(client: Client, message: Message):
    """
    Обрабатывает ввод пароля пользователя при регистрации.
    Завершается создание нового пользователя в базе данных.

    Аргументы:
        client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
        message (Message): Сообщение пользователя, содержащее пароль.

    Отправляет:
        Сообщение с подтверждением завершения регистрации и переходом в главное меню.
    """
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == RegistrationStates.WAITING_FOR_PASSWORD:
        user_password = message.text
        user_registration["password"] = user_password
        await UsersRepository().create_user(instance=user_registration)
        await message.reply(
            "Регистрация завершена ✅\n\n",
            parse_mode=enums.ParseMode.HTML
        )
    await main_menu_command(client, message)
