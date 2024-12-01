import logging

from pyrogram import Client, filters

from app.core.callbacks.auth_callback import registration_callback, login_callback
from app.core.callbacks.logout_callback import logout_callback
from app.core.callbacks.user_calback import user_profile_callback, update_user_name_callback, update_user_email_callback
from app.core.commands.manager_commands import commands_manager
from app.core.commands.auth.registration_commands import start_command
from app.core.filters.base_filter import dynamic_data_filter
from app.settings import logging_settings
from app.settings.config_settings import api_id, api_host, bot_token

""" Конфигурация клиента"""

app = Client(
    "tma_bot",  # Имя сессии
    api_id=api_id,
    api_hash=api_host,
    bot_token=bot_token
)


# COMMANDS

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await start_command(client, message)


# COMMANDS/registration
@app.on_message(filters.private)
async def commands_manager_handler(client, message):
    await commands_manager(client, message)


# CALLBACKS

# CALLBACKS/registration
@app.on_callback_query(dynamic_data_filter("registration"))
async def registration_callback_handler(client, callback_query):
    await registration_callback(client, callback_query)


# CALLBACKS/login
@app.on_callback_query(dynamic_data_filter("login"))
async def login_callback_handler(client, callback_query):
    await login_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("logout"))
async def logout_callback_handler(client, callback_query):
    await logout_callback(client, callback_query)


# CALLBACKS/user
@app.on_callback_query(dynamic_data_filter("my_profile"))
async def user_profile_callback_handler(client, callback_query):
    await user_profile_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("change_name"))
async def update_user_name_callback_handler(client, callback_query):
    await update_user_name_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("change_email"))
async def update_user_email_callback_handler(client, callback_query):
    await update_user_email_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("back"))
async def back_callback_handler(client, callback_query):
    await start_command(client, callback_query.message)


@app.on_callback_query(dynamic_data_filter("denied"))
async def denied_callback_handler(client, callback_query):
    await start_command(client, callback_query.message)


# Запуск клиента
if __name__ == "__main__":
    logging_settings.setup_logger()
    logging.info("Bot nachal rabotu !")
    app.run()
