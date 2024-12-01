from app.enums.base import BaseEnum


class UpdateUserStates(BaseEnum):
    WAITING_FOR_UPDATE_EMAIL = "waiting_for_update_email"
    WAITING_FOR_UPDATE_NAME = "waiting_for_update_name"
