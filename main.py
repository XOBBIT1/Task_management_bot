import logging

from pyrogram import Client, filters

from app.settings import logging_settings
from app.settings.config_settings import api_id, api_host, bot_token

""" Конфигурация клиента"""

app = Client(
    "tma_bot",  # Имя сессии
    api_id=api_id,
    api_hash=api_host,
    bot_token=bot_token
)


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply("Привет! Я бот, готов к работе 🚀")

# Запуск клиента
if __name__ == "__main__":
    logging_settings.setup_logger()
    logging.info("Bot nachal rabotu !")
    app.run()
