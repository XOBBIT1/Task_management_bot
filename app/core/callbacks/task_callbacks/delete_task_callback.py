from pyrogram import enums

from app.core.callbacks.task_callbacks.get_all_tasks_callback import tasks_main_menu_callback
from app.core.repositories.tasks import TasksRepository
from app.settings.config_settings import task_update


async def delete_task_callback(client, callback_query):
    task_id = callback_query.data.split('_')[2]
    updated_task = await TasksRepository().delete_task(
        task_id=int(task_id),
    )
    if updated_task:
        await callback_query.message.reply(
            f"<b>Задача {task_update["task_name"]} успешно удалена!</b>✅\n\n",
            parse_mode=enums.ParseMode.HTML
        )
        await tasks_main_menu_callback(client, callback_query)
