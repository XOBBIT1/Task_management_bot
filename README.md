# Task Managment Telegram Bot

## Описание проекта
### Общая информация
Этот проект представляет собой Telegram-бота, который помогает пользователям управлять своими задачами. Бот взаимодействует с пользователями через Telegram и хранит данные о задачах и пользователях в базе данных PostgreSQL. Бот предоставляет функциональность для создания, редактирования и удаления задач, а также для управления профилем пользователя (например, изменение имени, почты и т.д.).
_____
### Tехнологии и инструменты
#### В проекте использованы следующие технологии и инструменты:

- <b>Python 3.12</b>
- <b>Pyrogram</b>
- <b>SQLAlchemy</b>
- <b>PostgreSQL</b>
- <b>Docker</b>
- <b>Docker Compose</b>
_____
### Архитектура решения
Проект состоит из нескольких ключевых компонентов:

- **Telegram Bot**: Основной компонент, который взаимодействует с пользователем через Telegram. Бот обрабатывает команды, выполняет CRUD-операции с задачами и профилями пользователей.
- **PostgreSQL Database**: База данных для хранения информации о пользователях, задачах и их статусах.
- **API Layer**: Программный интерфейс для работы с базой данных и взаимодействия с ботом.
- **Docker**: Контейнеризация позволяет развернуть и изолировать базу данных и бота в контейнерах, что упрощает их настройку и запуск.
_____
### Диаграмма компонентов и взаимодействий


| Telegram User  <-----> Pyrogram Bot <----> Database (Postgres) |
|----------------------------------------------------------------|

____
### Описание основных классов и функций

#### Классы и их назначение
````
UserState:
````
*Хранит состояние пользователя в контексте работы бота. Например, если бот ожидает от пользователя ответ на определённый вопрос.*

#### Основные методы:
- set_state: Устанавливает состояние пользователя.
- get_state: Получает текущее состояние пользователя.
- clear_state: Очищает состояние пользователя.
````
DBSessionManager:
````
*Управляет сессиями базы данных, предоставляя асинхронный интерфейс для работы с базой данных.*

#### Основной метод:
- get_session(): Возвращает сессию для работы с базой данных.
````
UsersRepository:
````
*Обеспечивает доступ к данным пользователей в базе данных.*

#### Основные методы:
- create_user: Создаёт нового пользователя в базе данных.
- get_user_by_chat_id: Получает пользователя по его chat_id.
- verify_user: Проводит проверку email и пароля для аутентификации.
- update_user: Обновляет данные пользователя.
````
TasksRepository:
````
*Управляет задачами в базе данных.*
#### Основные методы:
- create_task: Создаёт новую задачу.
- get_task_by_id: Получает задачу по её ID.
- update_task: Обновляет информацию о задаче.
- delete_task: Удаляет задачу.


#### Telegram Bot:

Реализует основные команды бота, такие как создание, обновление и удаление задач, а также управление профилем пользователя.
Бот использует библиотеку Pyrogram для работы с Telegram API.
Подробное описание реализованной функциональности
Функции бота:
Регистрация пользователя: Пользователи могут зарегистрироваться, указав свой email и пароль. После регистрации бот сохраняет данные пользователя в базе.

##### Пример:

- ***Регистрация пользователя***: Пользователи могут зарегистрироваться, указав свой email и пароль. После регистрации бот сохраняет данные пользователя в базе.
````python
@app.on_callback_query(dynamic_data_filter("registration"))
async def handle_registration_callback(client, callback_query):
    await registration_callback(client, callback_query)
````

- ***Создание задачи***: Пользователи могут создавать задачи с указанием имени задачи и её описания.

````python
@app.on_callback_query(dynamic_data_filter("create_task"))
async def handle_create_task_callback(client, callback_query):
    await create_task_callback(client, callback_query)
````
- ***Просмотр задач***: Пользователи могут просматривать все свои задачи.

````python
@app.on_callback_query(dynamic_data_filter("my_tasks"))
async def handle_get_all_tasks_callback(client, callback_query):
    await get_all_tasks_callback(client, callback_query)
````

- ***Редактирование задач***: Пользователи могут редактировать статус или приоритет задач.

````python
@app.on_callback_query(dynamic_data_filter_startswith("change_task_"))
async def handle_update_task_callback(client, callback_query):
    await update_task_callback(client, callback_query)
````
- ***Обновление профиля***: Пользователи могут обновлять свои данные (например, имя или email).

````python
@app.on_callback_query(dynamic_data_filter("my_profile"))
async def handle_user_profile_callback(client, callback_query):
    await user_profile_callback(client, callback_query)
````

- ***Вход и выход из системы***: Пользователи могут войти в систему с помощью email и пароля. Также предусмотрена возможность выхода из системы.

````python
@app.on_callback_query(dynamic_data_filter("login"))
async def handle_login_callback(client, callback_query):
    await login_callback(client, callback_query)


@app.on_callback_query(dynamic_data_filter("logout"))
async def handle_logout_callback(client, callback_query):
    await logout_callback(client, callback_query)
````

### Описание SQL-запросов и структуры базы данных
#### Структура базы данных
Проект использует две основные таблицы:

##### Users:

- id: Уникальный идентификатор пользователя.
- name: Имя пользователя.
- email: Электронная почта пользователя.
- chat_id: Идентификатор пользователя в Telegram.
- created_at: Дата и время создания аккаунта.
- is_verified: Флаг, который указывает, прошёл ли пользователь верификацию.

##### Tasks:

- id: Уникальный идентификатор задачи.
- task_name: Название задачи.
- task_descriptions: Описание задачи.
- creator_id: Ссылка на пользователя, который создал задачу.
- created_at: Дата и время создания задачи.
- status: Статус задачи (например, "in progress", "completed").
- priority: Приоритет задачи.

### Пример SQL-запроса:
- Для получения всех задач пользователя:

````sql
SELECT * FROM tasks WHERE creator_id = ?;
Для создания нового пользователя:
````
````sql
INSERT INTO users (name, email, chat_id, created_at) VALUES (?, ?, ?, ?);
Инструкции по развертыванию и запуску
````

## Шаги для запуска проекта

### 1. Установите зависимостей

```bash
pipenv install
pipenv shell 

или 

pip install -r requirements.txt -> если дейлаеете своё виртуальное окружение 
```

### 2. Запуск проекта через Docker Compose

В корне проекта (там, где находится `docker-compose.yml`), выполните команду:

```bash
docker-compose up -d
```
Это запустит проект в docker-compose.yml.
