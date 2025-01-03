from sqlalchemy import text

from app.settings import config_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


class DBSessionManager:
    """
    Класс для управления асинхронными сессиями базы данных.

    Этот класс управляет подключением к базе данных и созданием сессий для выполнения асинхронных операций с использованием SQLAlchemy.

    Атрибуты:
        _engine (AsyncEngine): Асинхронный движок для подключения к базе данных.
        _AsyncSession (sessionmaker): Создатель асинхронных сессий для работы с базой данных.

    Методы:
        get_session() -> SessionContextManager:
            Возвращает контекстный менеджер для работы с асинхронной сессией.
    """
    def __init__(self,):
        self._engine = create_async_engine(config_settings.db_url, echo=True)
        self._AsyncSession = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    # Асинхронный контекстный менеджер для сессии
    class SessionContextManager:
        def __init__(self, session_maker: sessionmaker):
            self._sessionmaker = session_maker
            self._session = None

        async def __aenter__(self):
            self._session = self._sessionmaker()
            return self._session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                await self._session.rollback()
            await self._session.close()

    def get_session(self):
        return self.SessionContextManager(self._AsyncSession)

    async def execute_raw_sql(self, query: str, params: dict = None):
        """
        Выполняет произвольный SQL-запрос и возвращает результат.

        :param query: SQL-запрос в виде строки.
        :param params: Параметры для подстановки в запрос (по умолчанию None).
        :return: Результат выполнения запроса.
        """
        async with self.get_session() as session:
            result = await session.execute(text(query), params or {})
            return result.fetchall()
