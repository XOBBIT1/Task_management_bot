import logging
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from app.settings.db.models import Tasks
from app.settings.db.session_to_postgres import DBSessionManager


class TasksRepository:
    """
   Репозиторий для работы с задачами.

   Этот класс предоставляет методы для создания, получения, обновления и удаления задач.
   Вся работа с данными происходит через асинхронный доступ к базе данных с использованием сессий.

   Атрибуты:
       db_session_manager (DBSessionManager): Менеджер сессий базы данных для работы с сессиями.
   """

    def __init__(self):
        """
        Инициализация репозитория задач.

        Создает экземпляр менеджера сессий базы данных для работы с задачами.
        """
        self.db_session_manager = DBSessionManager()
        super().__init__()

    async def create_task(self, instance: dict, creator_id: int):
        """
           Создает новую задачу в базе данных.

           Аргументы:
               instance (dict): Словарь с данными для задачи, такими как название и описание.
               creator_id (int): Идентификатор пользователя, который создает задачу.

           Возвращает:
               Tasks: Созданная задача.
           SQL запрос:
                INSERT INTO tasks (task_name, task_descriptions, creator_id, created_at)
                VALUES (:task_name, :task_descriptions, :creator_id, :created_at)
                RETURNING id, task_name, task_descriptions, creator_id, created_at
        """
        async with self.db_session_manager.get_session() as session:
            try:
                new_task = Tasks(
                    task_name=instance.get("task_name"),
                    task_descriptions=instance.get("task_descriptions"),
                    creator_id=creator_id,
                    created_at=datetime.utcnow()
                )
                session.add(new_task)
                await session.commit()  # Асинхронный коммит
                await session.refresh(new_task)
                return new_task
            except Exception as e:
                logging.info(f"Failed to create task: {e}")
                await session.rollback()  # Откат при ошибке

    async def get_task_by_id(self, task_id: int):
        """
         Получает задачу по ее ID.

         Аргументы:
             task_id (int): Идентификатор задачи.

         Возвращает:
             Tasks или None: Задача с указанным ID, если она существует, иначе None.
         SQL запрос:
             "SELECT * FROM tasks WHERE id = :task_id"
         """
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Tasks).filter_by(id=task_id)
                result = await session.execute(query)
                task = result.scalars().first()
                # Получаем первый результат
                return task
            except NoResultFound as ex:
                logging.info(f"Task not found: {ex}")
                return None

    async def get_all_tasks(self,):
        """
        Получает все задачи из базы данных.

        Возвращает:
            List[Tasks]: Список всех задач.
        SQL запрос:
            "SELECT * FROM tasks"
        """
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Tasks)
                result = await session.execute(query)
                tasks = result.scalars().all()
                return tasks
            except NoResultFound as ex:
                raise Exception(f"User not found: {ex}")

    async def update_task(self, task_id: int, task_update_data):
        """
           Обновляет данные задачи по ее ID.

           Аргументы:
               task_id (int): Идентификатор задачи.
               task_update_data (dict): Словарь с обновленными данными для задачи.

           Возвращает:
               Tasks или None: Обновленная задача, если она существует и обновление прошло успешно, иначе None.
           SQL запрос:
              "UPDATE tasks SET priority = :priority WHERE id = :task_id"
           """
        async with self.db_session_manager.get_session() as session:
            try:
                print(task_update_data)
                task = await self.get_task_by_id(task_id)
                if not task:
                    logging.info(f"Task with id: {task_id} not found.")
                    return None
                if task_update_data.get("task_name") is not None:
                    task.task_name = task_update_data.get("task_name")
                if task_update_data.get("task_descriptions") is not None:
                    task.task_descriptions = task_update_data.get("task_descriptions")
                if task_update_data.get("status") is not None:
                    task.status = task_update_data.get("status")
                if task_update_data.get("priority") is not None:
                    task.priority = task_update_data.get("priority")
                session.add(task)
                await session.commit()
                await session.refresh(task)
                return task
            except Exception as ex:
                logging.error(f"Error updating task: {ex}")
                return None

    async def delete_task(self, task_id: int):
        """
           Удаляет задачу по ее ID.

           Аргументы:
               task_id (int): Идентификатор задачи для удаления.

           Возвращает:
               Tasks или None: Удаленная задача, если она была найдена и удалена, иначе None.

           SQL запрос:
            "DELETE FROM tasks WHERE id = :task_id"
        """
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Tasks).filter_by(id=task_id)
                result = await session.execute(query)
                task = result.scalars().first()

                if not task:
                    logging.info(f"Task with id: {task_id} not found.")
                    return None
                await session.delete(task)
                await session.commit()
                return task
            except Exception as ex:
                logging.error(f"Error deleting task: {ex}")
