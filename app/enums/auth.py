from app.enums.tasks import BaseEnum


class RegistrationStates(BaseEnum):
    WAITING_FOR_NAME = "waiting_for_name"
    WAITING_FOR_EMAIL = "waiting_for_email"
    WAITING_FOR_PASSWORD = "waiting_for_password"


class LoginStates(BaseEnum):
    WAITING_FOR_LOGING_EMAIL = "waiting_for_loging_email"
    WAITING_FOR_LOGING_PASSWORD = "waiting_for_loging_password"
