# Используем официальный образ Python
FROM python:3.12

# Устанавливаем необходимые пакеты, включая netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости через pipenv
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Копируем и делаем исполнимым файл entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Указываем точку входа в контейнер
ENTRYPOINT ["/entrypoint.sh"]
