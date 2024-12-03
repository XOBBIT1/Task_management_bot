import logging
import os

import dotenv
from pathlib import Path

from pyrogram import Client

from app.settings.state import UserState

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")
logger = logging.getLogger()


if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# bot_settings

api_host = os.environ["APP_HOST"]
api_id = os.environ["APP_ID"]
bot_token = os.environ["BOT_TOKEN"]
user_state = UserState()
user_registration = dict()
user_update = dict()
user_login = dict()
create_task = dict()
task_update = dict()

app_client = Client(
    "tma_bot",  # Имя сессии
    api_id=api_id,
    api_hash=api_host,
    bot_token=bot_token
)


# bd_settings
host = os.environ['HOST']
user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
port = os.environ["PORT"]
db_url = os.environ["DB_URL"]
