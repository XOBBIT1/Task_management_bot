from pyrogram import enums

from app.core.keyboards.auth_keyboard import auth_keyboard, denied_keyboard, loging_keyboard, main_menu_keyboard
from app.core.repositories.users import UsersRepository
from app.enums.auth import RegistrationStates
from app.settings.config_settings import user_state, user_registration


async def try_again_registration(client, message):
    user_id = message.from_user.id
    user_state.set_state(user_id, RegistrationStates.WAITING_FOR_EMAIL)
    await message.reply(
        "Введите <b>Вашу почту</b> ✍️\n\n"
        "Пример: <i>example@mail.com</i>",
        parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
    )


async def start_command(client, message):
    user = await UsersRepository().user_is_verified(chat_id=message.chat.id)
    if user:
        await message.reply(
            "🟢\n\n"
            f"Привет {message.from_user.first_name}!\n\n"
            "Добро пожаловать в TaskManager Pro! 🎯\n\n"
            "Организуйте задачи, улучшайте командное взаимодействие и достигайте целей эффективнее!\n"
            "<ul><li>✨ Возможности системы:\n\n</li>"
            "<li>📋 Создавайте и управляйте задачами.\n</li>"
            "<li>👥 Отслеживайте прогресс выполнения задач.\n</li>"
            "<li>📊 Анализируйте результаты работы.</li></ul>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=main_menu_keyboard()
        )
    else:
        await message.reply(
            "🔴\n\n"
            f"Привет <b>{message.from_user.first_name}!</b>\n\n"
            f"Добро пожаловать в TaskManager! 🎯\n\n"
            f"<b>🔑 Вы впервые у нас?</b>\n"
            f"Зарегистрируйтесь, чтобы начать управлять и создавать собственне задачами!\n\n"
            f"<b>👋 Уже зарегистрированы?</b>\n"
            f"Просто войдите в систему и продолжите работу над Вашими проектами!\n\n"
            f"<b>✨ Начните прямо сейчас и кликайте:</b>\n"
            f"<i>1️⃣ Регистрация: Создайте учетную запись за минуту.</i>\n"
            f"<i>2️⃣ Вход: Используйте свои учетные данные для доступа.</i>\n\n"
            f"<b>Управляйте своими задачами легко и эффективно!</b> 🚀",
            parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard()
        )


async def main_menu_command(client, message):
    await message.reply(
        "<b>Поздравляю с упешной регистарциее! 🎊🎊🎊\n\n</b>"
        "Осталось просто войти в систему и продолжать работу над Вашими проектами!\n\n"
        "<b>✨ Начните прямо сейчас и кликайте:</b>\n"
        "<i>1️⃣ Вход: Используйте свои учетные данные для доступа.</i>\n\n"
        "<b>Управляйте своими задачами легко и эффективно!</b> 🚀",
        parse_mode=enums.ParseMode.HTML, reply_markup=loging_keyboard()
    )


async def registration_get_name(client, message):
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


async def registration_get_email(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == RegistrationStates.WAITING_FOR_EMAIL:
        user_email = message.text
        user_registration["email"] = user_email
        user = await UsersRepository().get_user_by_email(email=user_email)
        if user:
            await message.reply(
                "Пользовтель с такой почтой уже существует!\n\n"
                "<b>Напишите другую почту</b>",
                parse_mode=enums.ParseMode.HTML
            )
            await try_again_registration(client, message)
            raise Exception("User with such email already exists")
        else:
            user_state.set_state(user_id, RegistrationStates.WAITING_FOR_PASSWORD)
            await message.reply(
                "Отлично осталось только придумать пароль!\n"
                "<b>НИКОМУ НЕ СООБЩАЙТЕ ЕГО 🤫</b>\n\n"
                "Пример: <i>AWD-dwdw212_1_@</i>",
                parse_mode=enums.ParseMode.HTML, reply_markup=denied_keyboard()
            )


async def registration_get_password(client, message):
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
