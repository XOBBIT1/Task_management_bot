import logging
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from app.settings.db.models import Tasks
from app.settings.db.session_to_postgres import DBSessionManager


class TasksRepository:

    def __init__(self):
        self.db_session_manager = DBSessionManager()
        super().__init__()

    async def create_task(self, instance: dict, creator_id: int):
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

    # async def get_task_by_task_name(self, task_name: str):
    #     async with self.db_session_manager.get_session() as session:
    #         try:
    #             query = select(Tasks).filter_by(task_name=task_name)
    #             result = await session.execute(query)
    #             task = result.scalars().first()
    #             return task
    #         except NoResultFound as ex:
    #             logging.info(f"User not found: {ex}")
    #             return None
    #
    async def get_all_tasks(self,):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Tasks)
                result = await session.execute(query)
                tasks = result.scalars().all()
                return tasks
            except NoResultFound as ex:
                raise Exception(f"User not found: {ex}")
    #
    # async def update_task(self, task_id: int, task_update_data):
    #     async with self.db_session_manager.get_session() as session:
    #         try:
    #             task = await self.get_task_by_id(task_id)
    #             if not task:
    #                 logging.info(f"Task with id: {task_id} not found.")
    #                 return None
    #             if task_update_data.task_name is not None:
    #                 task.task_name = task_update_data.task_name
    #             if task_update_data.task_descriptions is not None:
    #                 task.task_descriptions = task_update_data.task_descriptions
    #             if task_update_data.status is not None:
    #                 task.status = task_update_data.status
    #             if task_update_data.priority is not None:
    #                 task.priority = task_update_data.priority
    #             session.add(task)
    #             await session.commit()
    #             await session.refresh(task)
    #             return task
    #         except Exception as ex:
    #             logging.error(f"Error updating user: {ex}")
    #             return None
    #
    # async def delete_task(self, task_id: int):
    #     async with self.db_session_manager.get_session() as session:
    #         try:
    #             query = select(Tasks).filter_by(id=task_id)
    #             result = await session.execute(query)
    #             task = result.scalars().first()
    #
    #             if not task:
    #                 logging.info(f"Task with id: {task_id} not found.")
    #                 return None
    #             await session.delete(task)
    #             await session.commit()
    #             return task
    #         except Exception as ex:
    #             logging.error(f"Error deleting task: {ex}")
