#!/bin/bash

# Ожидание доступности базы данных перед запуском приложения
echo "Waiting for the database to be ready..."
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL connection..."
  sleep 1
done

# Активируем виртуальное окружение pipenv и запускаем бота
echo "Database is ready, starting the bot..."
pipenv run python /app/main.py  # Убедитесь, что путь к вашему файлу правильный

# Ожидаем, чтобы контейнер продолжал работать после завершения бота
tail -f /dev/null
