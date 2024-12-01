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
                logging.info(f"function: create_user\n\n"
                             f"Failed to create user: {e}")
                await session.rollback()

    async def get_user_by_chat_id(self, chat_id):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Users).filter_by(chat_id=chat_id)
                result = await session.execute(query)
                user = result.scalars().first()
                return user
            except Exception as e:
                logging.info(f"function: get_user_by_chat_id\n\n"
                             f"Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке

    async def get_user_by_email(self, email):
        async with self.db_session_manager.get_session() as session:
            try:
                query = select(Users).filter_by(email=email)
                result = await session.execute(query)
                user = result.scalars().first()
                return user
            except Exception as e:
                logging.info(f"function: get_user_by_email\n\n"
                             f"Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке

    async def user_is_verified(self, chat_id):
        async with self.db_session_manager.get_session() as session:
            try:
                user = await self.get_user_by_chat_id(chat_id)
                if user.is_verified:
                    return user
                else:
                    raise Exception("User hasn't verified")
            except Exception as e:
                logging.info(f"function: user_is_verified\n\n"
                             f"Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке

    async def verify_user(self, email, password):
        async with self.db_session_manager.get_session() as session:
            try:
                user = await self.get_user_by_email(email)
                if not user:
                    raise Exception(f"User with such {email} does not exist")
                if not pwd_context.verify(password, user.password):
                    raise Exception("Incorrect password")
                user.is_verified = True
                user = await session.merge(user)
                await session.commit()  # Асинхронный коммит
                await session.refresh(user)  # Обновление объекта с новыми данными из базы
                return user
            except Exception as e:
                logging.info(f"function: verify_user\n\n"
                             f" Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке

    async def user_logout(self, chat_id):
        async with self.db_session_manager.get_session() as session:
            try:
                user = await self.get_user_by_chat_id(chat_id)
                if not user:
                    raise Exception(f"User with such {chat_id} does not exist")
                user.is_verified = False
                user = await session.merge(user)
                await session.commit()  # Асинхронный коммит
                await session.refresh(user)  # Обновление объекта с новыми данными из базы
                return user
            except Exception as e:
                logging.info(f"function: user_logout\n\n"
                             f" Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке

    async def update_user(self, chat_id, user_data: dict):
        async with self.db_session_manager.get_session() as session:
            try:
                user = await self.get_user_by_chat_id(chat_id)
                if not user:
                    raise Exception(f"User with such {chat_id} does not exist")
                if user_data.get("name") is not None:
                    user.name = user_data.get("name")
                if user_data.get("email") is not None:
                    user.email = user_data.get("email")
                user = await session.merge(user)
                await session.commit()  # Асинхронный коммит
                await session.refresh(user)  # Обновление объекта с новыми данными из базы
                return user
            except Exception as e:
                logging.info(f"function: update_user\n\n"
                             f" Failed to fiend user: {e}")
                await session.rollback()  # Откат при ошибке
