from pyrogram import enums, Client, types

from app.core.callbacks.task_callbacks.main_menu_callback import tasks_main_menu_callback
from app.core.repositories.tasks import TasksRepository
from app.settings.config_settings import task_update


async def delete_task_callback(client: Client, callback_query: types.CallbackQuery):
    """
   Обрабатывает callback для удаления задачи. Функция извлекает ID задачи из данных callback,
   удаляет задачу из базы данных и отправляет уведомление пользователю о подтверждении удаления.
   Затем пользователь перенаправляется в главное меню задач.

   Аргументы:
       client (Client): Экземпляр клиента Pyrogram, используемый для отправки сообщений.
       callback_query (CallbackQuery): Callback запрос, содержащий ID задачи, которую необходимо удалить.

   Отправляет:
       Сообщение подтверждения пользователю о том, что задача была успешно удалена и
       перенаправляет в главное меню задач.
   """
    task_id = callback_query.data.split('_')[2]
    task_name = task_update["task_name"]
    updated_task = await TasksRepository().delete_task(
        task_id=int(task_id),
    )
    if updated_task:
        await callback_query.message.reply(
            f"<b>Задача {task_name} успешно удалена!</b>✅\n\n",
            parse_mode=enums.ParseMode.HTML
        )
        await tasks_main_menu_callback(client, callback_query)
