
from app.enums.base import BaseEnum


class TaskStatus(BaseEnum):
    NEW = "Новая задача"
    INPROGRESS = "В разработке"
    COMPLETED = "Выполненная задача"


class TaskPriority(BaseEnum):
    LOW = "Низкий"
    MIDDLE = "Средний"
    HIGH = "Высокий"


class UserTasksStates(BaseEnum):
    WAITING_FOR_TASK_NAME = "waiting_for_task_name"
    WAITING_FOR_TASK_DESCRIPTION = "waiting_for_task_description"
    WAITING_FOR_TASK_UPDATE_DESCRIPTION = "waiting_for_task_update_description"
    WAITING_FOR_TASK_UPDATE_NAME = "waiting_for_task_update_name"
