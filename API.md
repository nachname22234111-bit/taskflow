# TaskFlow API

## Назначение и общие правила

Это проектный контракт для реализации, а не результат проверки работающего сервера. Базовый URL локального сервера: `http://127.0.0.1:5000`. Префикс `/api` не используется. Контракт продолжает схему БД предыдущей работы.

JSON-запросы отправляются с `Content-Type: application/json`. Все операции `/tasks` требуют `Authorization: Bearer <token>`. Регистрация и вход доступны без токена. Пользователь работает только с доступными ему проектами; точную модель совместного доступа необходимо реализовать на сервере.

`id` в пути — положительное целое число. Статусы: `new`, `in_progress`, `done`; приоритеты: `low`, `medium`, `high`. `deadline` — дата и время ISO 8601 или null. Пустой title недопустим. `project_id` и ненулевой `assignee_id` должны ссылаться на существующие записи. Поля id и created_at назначает сервер.

Единый пример ошибки (HTTP 404):

```json
{"error": {"code": "not_found", "message": "Задача не найдена"}}
```

## Эндпоинты

### POST /auth/register

Регистрация пользователя.

Тело запроса:

```json
{
  "username": "tikhon",
  "email": "tikhon@example.com",
  "password": "StudyPass2026!"
}
```

Ответ: HTTP 201.

```json
{
  "id": 1,
  "username": "tikhon",
  "email": "tikhon@example.com"
}
```

Обязательны username, email и password. Пароль не возвращается. Ошибки: 400 — неверные поля, 409 — имя или email заняты.

### POST /auth/login

Получение токена доступа.

Тело запроса:

```json
{
  "email": "tikhon@example.com",
  "password": "StudyPass2026!"
}
```

Ответ: HTTP 200.

```json
{
  "token": "example_access_token",
  "user_id": 1
}
```

Обязательны email и password. Значение токена иллюстративное. Ошибки: 400 — неверные поля, 401 — неверные учётные данные.

### GET /tasks

Получение доступных пользователю задач.

Тело запроса отсутствует.

Ответ: HTTP 200.

```json
[
  {
    "id": 1,
    "title": "Подготовить отчёт",
    "description": "Лабораторная работа № 3",
    "status": "new",
    "priority": "medium",
    "project_id": 1,
    "assignee_id": 1,
    "created_at": "2026-10-11T10:00:00Z",
    "deadline": null
  }
]
```

При отсутствии задач возвращается пустой массив []. Ошибка: 401 — отсутствующий или недействительный токен.

### POST /tasks

Создание задачи.

Тело запроса:

```json
{
  "title": "Подготовить отчёт",
  "description": "Лабораторная работа № 3",
  "status": "new",
  "priority": "medium",
  "project_id": 1,
  "assignee_id": 1,
  "deadline": null
}
```

Ответ: HTTP 201.

```json
{
  "id": 1,
  "title": "Подготовить отчёт",
  "description": "Лабораторная работа № 3",
  "status": "new",
  "priority": "medium",
  "project_id": 1,
  "assignee_id": 1,
  "created_at": "2026-10-11T10:00:00Z",
  "deadline": null
}
```

Обязательны title и project_id. По умолчанию status=new, priority=medium; description, assignee_id и deadline могут быть null. Ошибки: 400 — неверные поля, 401 — нет авторизации, 403 — нет доступа к проекту, 404 — проект или исполнитель не найден.

### GET /tasks/{id}

Получение одной задачи.

Тело запроса отсутствует.

Ответ: HTTP 200.

```json
{
  "id": 1,
  "title": "Подготовить отчёт",
  "description": "Лабораторная работа № 3",
  "status": "new",
  "priority": "medium",
  "project_id": 1,
  "assignee_id": 1,
  "created_at": "2026-10-11T10:00:00Z",
  "deadline": null
}
```

Пример URL: /tasks/1. Ошибки: 401 — нет авторизации, 403 — нет доступа, 404 — задача не найдена.

### PUT /tasks/{id}

Полная замена изменяемых полей задачи.

Тело запроса:

```json
{
  "title": "Подготовить отчёт",
  "description": "Лабораторная работа № 3",
  "status": "done",
  "priority": "medium",
  "project_id": 1,
  "assignee_id": 1,
  "deadline": null
}
```

Ответ: HTTP 200.

```json
{
  "id": 1,
  "title": "Подготовить отчёт",
  "description": "Лабораторная работа № 3",
  "status": "done",
  "priority": "medium",
  "project_id": 1,
  "assignee_id": 1,
  "created_at": "2026-10-11T10:00:00Z",
  "deadline": null
}
```

Передаются все семь изменяемых полей из примера. id и created_at не изменяются. Ошибки: 400 — неверные поля, 401 — нет авторизации, 403 — нет доступа, 404 — задача или связанная сущность не найдена.

### DELETE /tasks/{id}

Удаление задачи и её комментариев.

Тело запроса отсутствует.

Ответ: HTTP 204.

Тело ответа отсутствует; JSON не возвращается.

Успешный ответ не содержит тела. Ошибки: 401 — нет авторизации, 403 — нет доступа, 404 — задача не найдена.

