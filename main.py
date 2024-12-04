import logging

from pyrogram import filters

from app.core.callbacks.auth_callback import registration_callback, login_callback
from app.core.callbacks.logout_callback import logout_callback
from app.core.callbacks.task_callbacks.create_task_callback import create_task_callback
from app.core.callbacks.task_callbacks.delete_task_callback import delete_task_callback
from app.core.callbacks.task_callbacks.get_all_tasks_callback import get_all_tasks_callback
from app.core.callbacks.task_callbacks.main_menu_callback import tasks_main_menu_callback
from app.core.callbacks.task_callbacks.update_task_callback import (
    update_task_callback, update_name_task_callback, update_desc_task_callback,
    update_priority_task_callback, update_status_task_callback, update_priority_callback,
    update_status_callback
)
from app.core.callbacks.user_calback import user_profile_callback, update_user_name_callback, update_user_email_callback
from app.core.commands.manager_commands import commands_manager
from app.core.commands.menu_commands import start_command
from app.core.filters.base_filter import dynamic_data_filter, dynamic_data_filter_startswith
from app.settings import logging_settings
from app.settings.config_settings import app_client

""" Конфигурация клиента"""

app = app_client


# COMMANDS

@app.on_message(filters.command("start") & filters.private)
async def handle_start_command(client, message):
    await start_command(client, message)


# COMMANDS/registration
@app.on_message(filters.private)
async def handle_commands_manager(client, message):
    await commands_manager(client, message)


# CALLBACKS

# CALLBACKS/registration
@app.on_callback_query(dynamic_data_filter("registration"))
async def handle_registration_callback(client, callback_query):
    await registration_callback(client, callback_query)


# CALLBACKS/login
@app.on_callback_query(dynamic_data_filter("login"))
async def handle_login_callback(client, callback_query):
    await login_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("logout"))
async def handle_logout_callback(client, callback_query):
    await logout_callback(client, callback_query)


# CALLBACKS/user
@app.on_callback_query(dynamic_data_filter("my_profile"))
async def handle_user_profile_callback(client, callback_query):
    await user_profile_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("change_name"))
async def handle_update_user_name_callback(client, callback_query):
    await update_user_name_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("change_email"))
async def handle_update_user_email_callback(client, callback_query):
    await update_user_email_callback(client, callback_query)


# CALLBACKS/task
@app.on_callback_query(dynamic_data_filter("tasks_management"))
async def handle_tasks_main_menu_callback(client, callback_query):
    await tasks_main_menu_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("create_task"))
async def handle_create_task_callback(client, callback_query):
    await create_task_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("my_tasks"))
async def handle_get_all_tasks_callback(client, callback_query):
    await get_all_tasks_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter_startswith("change_task_"))
async def handle_update_task_callback(client, callback_query):
    await update_task_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("update_task_name"))
async def handle_update_task_name_callback(client, callback_query):
    await update_name_task_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("update_task_desc"))
async def handle_update_task_description_callback(client, callback_query):
    await update_desc_task_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("update_task_priority"))
async def handle_update_task_priority_callback(client, callback_query):
    await update_priority_task_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("update_task_status"))
async def handle_update_task_status_callback(client, callback_query):
    await update_status_task_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter_startswith("status_"))
async def handler_update_status_callback(client, callback_query):
    await update_status_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter_startswith("priority_"))
async def handler_update_priority_callback(client, callback_query):
    await update_priority_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter_startswith("delete_task_"))
async def handle_delete_task_callback(client, callback_query):
    await delete_task_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("back"))
async def handle_back_navigation(client, callback_query):
    await start_command(client, callback_query.message)


@app.on_callback_query(dynamic_data_filter("denied"))
async def handle_access_denied(client, callback_query):
    await start_command(client, callback_query.message)


# Запуск клиента
if __name__ == "__main__":
    logging_settings.setup_logger()
    logging.info("Bot nachal rabotu !")
    app.run()
