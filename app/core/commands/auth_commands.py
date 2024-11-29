from pyrogram import enums

from app.core.keyboards.auth_keyboard import auth_keyboard, denied_keyboard, main_menu_keyboard
from app.core.repositories.users import UsersRepository
from app.enums.auth import RegistrationStates
from app.settings.config_settings import user_state, user_data


async def start_command(client, message):
    user = await UsersRepository().user_is_verified(chat_id=message.chat.id)
    if user:
        await message.reply(
            f"Привет {message.from_user.first_name}!\n\n"
            f"Добро пожаловать в TaskManager Pro! 🎯\n\n"
            f"Организуйте задачи, улучшайте командное взаимодействие и достигайте целей эффективнее!\n"
            f"✨ Возможности системы:\n\n"
            f"📋 Создавайте и управляйте задачами.\n"
            f"👥 Делитесь задачами с командой и отслеживайте прогресс.\n"
            f"🔔 Получайте уведомления о важных событиях.\n"
            f"📊 Анализируйте результаты работы.", parse_mode=enums.ParseMode.HTML, reply_markup=auth_keyboard()
        )
    else:
        await message.reply(
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
        parse_mode=enums.ParseMode.HTML, reply_markup=main_menu_keyboard()
    )


async def registration_get_name(client, message):
    user_data["username"] = message.from_user.username
    user_data["chat_id"] = message.chat.id
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state == RegistrationStates.WAITING_FOR_NAME:
        name = message.text
        user_data["name"] = name
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
        user_data["email"] = user_email
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
        user_data["password"] = user_password
        await UsersRepository().create_user(instance=user_data)
        await message.reply(
            "Регистрация завершена ✅\n\n",
            parse_mode=enums.ParseMode.HTML
        )
    await main_menu_command(client, message)


async def start_registration(client, message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    if state == RegistrationStates.WAITING_FOR_NAME:
        await registration_get_name(client, message)
    elif state == RegistrationStates.WAITING_FOR_EMAIL:
        await registration_get_email(client, message)
    elif state == RegistrationStates.WAITING_FOR_PASSWORD:
        await registration_get_password(client, message)
