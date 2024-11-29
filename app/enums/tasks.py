
from app.enums.base import BaseEnum


class TaskStatus(BaseEnum):
    NEW = "Новая задача"
    IN_PROGRESS = "В разработке"
    COMPLETED = "Выполненная задача"


class TaskPriority(BaseEnum):
    LOW = "Низкий"
    MIDDLE = "Средний"
    HIGH = "Высокий"
