from datetime import datetime
from sqlalchemy import Enum

from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import relationship

from app.enums.tasks import TaskStatus, TaskPriority

Base = declarative_base()


class Tasks(Base):
    __tablename__ = 'Tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column("task_name", db.String)
    task_descriptions = db.Column("task_descriptions", db.String)
    status = db.Column(Enum(TaskStatus, native_enum=False), default=TaskStatus.NEW, nullable=False)
    priority = db.Column(Enum(TaskPriority, native_enum=False), default=TaskPriority.LOW, nullable=False)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow())
    creator_id = db.Column(db.BigInteger, db.ForeignKey("Users.id"))  # Внешний ключ, связывающий задачу с пользователем
    creator = relationship("Users", back_populates="tasks")  # Отношение к пользователю

    @property
    def readable_status(self):
        return {
            TaskStatus.NEW: "Новая",
            TaskStatus.IN_PROGRESS: "В процессе",
            TaskStatus.COMPLETED: "Завершена"
        }.get(self.status, "Неизвестный статус")

    @property
    def readable_priority(self):
        return {
            TaskPriority.LOW: "Низкий",
            TaskPriority.MIDDLE: "Средний",
            TaskPriority.HIGH: "Высокий"
        }.get(self.priority, "Неизвестный приоритет")


class Users(Base):
    __tablename__ = "Users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column("name", db.String)
    username = db.Column("username", db.String)
    password = db.Column("password", db.String)
    email = db.Column("email", db.String)
    chat_id = db.Column("chat_id", db.BigInteger)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow())
    is_verified = db.Column("is_verified", db.Boolean, default=False)
    tasks = relationship("Tasks", back_populates="creator")
