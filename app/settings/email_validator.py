from email_validator import validate_email, EmailNotValidError


async def validate_user_email(email: str) -> bool:
    """
       Проверяет, является ли указанный email валидным.

       Использует библиотеку `email-validator` для проверки правильности email адреса.

       Аргументы:
           email (str): Электронная почта пользователя, которую нужно проверить.

       Возвращает:
           bool: True, если email валиден, иначе False.
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
