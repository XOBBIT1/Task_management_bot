from pyrogram import Client, enums
from pyrogram.types import Message

from app.core.keyboards.auth_keyboard import loging_keyboard, auth_keyboard, main_menu_keyboard
from app.core.repositories.users import UsersRepository


async def start_command(client: Client, message: Message):
    """
      Обрабатывает команду /start в боте.

      Если пользователь уже зарегистрирован и подтвержден, отправляет приветственное сообщение с основными функциями
      системы и клавиатурой для основного меню. Если пользователь не зарегистрирован, предлагает зарегистрироваться
      или войти, показывая соответствующую клавиатуру.

      Args:
          client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
          message (Message): Объект сообщения, представляющий команду /start от пользователя.
      """
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


async def main_menu_command(client: Client, message: Message):
    """
      Обрабатывает команду для отображения основного меню.

      Отправляет сообщение с поздравлением после успешной регистрации и предлагает пользователю войти в систему.
      Включает клавиатуру для входа.

      Args:
          client (Client): Клиент Pyrogram для взаимодействия с Telegram API.
          message (Message): Объект сообщения, инициировавший запрос.
      """
    await message.reply(
        "<b>Поздравляю с упешной регистарциее! 🎊🎊🎊\n\n</b>"
        "Осталось просто войти в систему и продолжать работу над Вашими проектами!\n\n"
        "<b>✨ Начните прямо сейчас и кликайте:</b>\n"
        "<i>1️⃣ Вход: Используйте свои учетные данные для доступа.</i>\n\n"
        "<b>Управляйте своими задачами легко и эффективно!</b> 🚀",
        parse_mode=enums.ParseMode.HTML, reply_markup=loging_keyboard()
    )
