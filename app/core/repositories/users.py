import logging
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy.future import select

from app.settings.db.models import Users
from app.settings.db.session_to_postgres import DBSessionManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersRepository:

    def __init__(self):
        self.db_session_manager = DBSessionManager()
        super().__init__()

    async def create_user(self, instance: dict):
        async with self.db_session_manager.get_session() as session:
            try:
                print(instance)
                hashed_password = pwd_context.hash(instance.get("password"))
                new_user = Users(
                    name=instance.get("name"),
                    username=instance.get("username"),
                    password=hashed_password,
                    email=instance.get("email"),
                    chat_id=instance.get("chat_id"),
                    created_at=datetime.utcnow(),
                )
                session.add(new_user)
                await session.commit()  # Асинхронный коммит
                await session.refresh(new_user)  # Обновление объекта с новыми данными из базы
                return logging.info("Successfully created")
            except Exception as e:
                logging.info(f"Failed to create user: {e}")
                await session.rollback()

    async def get_user_by_chat_id(self, cat_id):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Users).filter_by(cat_id=cat_id)
                result = await session.execute(query)
                user = result.scalars().first()
                return user
            except Exception as e:
                logging.info(f"Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке

    async def user_is_verified(self, chat_id):
        async with self.db_session_manager.get_session() as session:
            try:
                user = await self.get_user_by_chat_id(chat_id)
                if user.is_verified:
                    return user
                else:
                    return "User hasn't verified"
            except Exception as e:
                logging.info(f"Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке
