import logging
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy.future import select

from app.settings.db.models import Users
from app.settings.db.session_to_postgres import DBSessionManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsersRepository:
    """
    Репозиторий для работы с пользователями.

    Этот класс предоставляет методы для создания, получения, обновления и удаления пользователей.
    Вся работа с данными происходит через асинхронный доступ к базе данных с использованием сессий.

    Атрибуты:
        db_session_manager (DBSessionManager): Менеджер сессий базы данных для работы с сессиями.
    """

    def __init__(self):
        """
       Инициализация репозитория пользователей.

       Создает экземпляр менеджера сессий базы данных для работы с пользователями.
       """
        self.db_session_manager = DBSessionManager()
        super().__init__()

    async def create_user(self, instance: dict):
        """
      Создает нового пользователя в базе данных.

      Аргументы:
          instance (dict): Словарь с данными для пользователя, такими как имя, почта, и т. д.

      Возвращает:
          None: Успешно создает пользователя, логирует успех.
      """
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
        """
           Получает пользователя по его chat_id.

           Аргументы:
               chat_id (int): Идентификатор чата пользователя.

           Возвращает:
               Users или None: Пользователь с указанным chat_id, если он существует, иначе None.
        """
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
        """
        Получает пользователя по его email.

        Аргументы:
            email (str): Адрес электронной почты пользователя.

        Возвращает:
            Users или None: Пользователь с указанным email, если он существует, иначе None.
        """
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
        """
       Проверяет, прошел ли пользователь верификацию.

       Аргументы:
           chat_id (int): Идентификатор чата пользователя.

       Возвращает:
           Users: Если пользователь верифицирован, возвращает его данные.
           Исключение: Если пользователь не верифицирован, выбрасывает исключение.
       """
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
        """
       Верифицирует пользователя по email и паролю.

       Аргументы:
           email (str): Адрес электронной почты пользователя.
           password (str): Пароль пользователя.

       Возвращает:
           Users: Если верификация успешна, возвращает данные пользователя.
           Исключение: Если пользователь не найден или пароль неверен, выбрасывает исключение.
       """
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
        """
       Осуществляет выход пользователя из системы, снимая верификацию.

       Аргументы:
           chat_id (int): Идентификатор чата пользователя.

       Возвращает:
           Users: Обновленные данные пользователя.
           Исключение: Если пользователь не найден, выбрасывает исключение.
       """
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
        """
       Обновляет данные пользователя.

       Аргументы:
           chat_id (int): Идентификатор чата пользователя.
           user_data (dict): Словарь с данными для обновления (например, имя, email).

       Возвращает:
           Users: Обновленные данные пользователя.
           Исключение: Если пользователь не найден, выбрасывает исключение.
       """
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
