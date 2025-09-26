# QA FastAPI - API для вопросов и ответов

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

REST API сервис для управления вопросами и ответами, построенный на FastAPI с использованием PostgreSQL.
## 🚀 Возможности

- ✅ Создание и управление вопросами
- ✅ Добавление ответов к вопросам  
- ✅ Пагинация и фильтрация
- ✅ Валидация данных (текст вопросов/ответов, UUID пользователя)
- ✅ Каскадное удаление вопросов с ответами
- ✅ Полностью асинхронная архитектура
- ✅ Документация API (Swagger/OpenAPI)
- ✅ Docker контейнеризация
- ✅ Автоматические миграции БД
- ✅ Логирование операций

## 📚 API Endpoints

### Вопросы (Questions)

| Метод | Endpoint | Описание | Статус |
|-------|----------|----------|--------|
| `GET` | `/api/v1/questions` | Получить список вопросов с пагинацией | ✅ |
| `POST` | `/api/v1/questions` | Создать новый вопрос | ✅ |
| `GET` | `/api/v1/questions/{id}` | Получить вопрос с ответами | ✅ |
| `DELETE` | `/api/v1/questions/{id}` | Удалить вопрос (каскадно удаляет ответы) | ✅ |

### Ответы (Answers)

| Метод | Endpoint | Описание | Статус |
|-------|----------|----------|--------|
| `POST` | `/api/v1/questions/{id}/answers` | Добавить ответ к вопросу | ✅ |
| `GET` | `/api/v1/answers/{id}` | Получить ответ по ID | ✅ |
| `DELETE` | `/api/v1/answers/{id}` | Удалить ответ | ✅ |

## 🛠 Технологии

- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+ с асинхронной поддержкой
- **Migrations**: Alembic с автогенерацией
- **Validation**: Pydantic v2 с кастомными валидаторами
- **Containerization**: Docker + Docker Compose
- **Testing**: Ручные API тесты (httpx + asyncio)

## 📦 Быстрый запуск

### Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+

### Запуск в Docker (рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd qa-fastapi
```

2. **Настройте окружение:**
```bash
cp .env.example .env
# Отредактируйте .env при необходимости
```

3. **Запустите приложение:**
```bash
docker-compose up -d
```

4. **Приложение будет доступно по адресам:**
   - API Documentation: http://localhost:8000/docs
   - API: http://localhost:8000/api/v1
   - PGAdmin: http://localhost:8080 (admin@qa.com / admin)

### Проверка работы

```bash
# Проверка API
curl http://localhost:8000/

# Запуск тестов
docker-compose exec app python test_api.py
```

## 🗄 Структура проекта

```
qa-fastapi/
├── app/
│   ├── api/              # FastAPI роутеры
│   ├── database/         # Модели и подключение к БД
│   ├── repository/       # Data Access Layer
│   ├── services/         # Бизнес-логика
│   ├── schemes/          # Pydantic схемы
│   └── main.py          # Точка входа
├── alembic/             # Миграции БД
├── tests/               # API тесты
├── docker-compose.yml   # Docker оркестрация
├── Dockerfile          # Образ приложения
├── requirements.txt    # Зависимости
└── test_api.py        # Ручные тесты API
```

## 📋 Примеры использования

### Создание вопроса

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/questions' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Как работает FastAPI?"
}'
```

### Добавление ответа

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/questions/1/answers' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "FastAPI - современный фреймворк для Python"
}'
```

### Получение вопроса с ответами

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/questions/1' \
  -H 'Content-Type: application/json'
```

## 🧪 Тестирование

### Запуск автоматических тестов

```bash
# Запуск внутри Docker контейнера
docker-compose exec app python test_api.py

# Локальный запуск (требует запущенной БД)
python test_api.py
```

### Тестовое покрытие

Тесты проверяют:
- ✅ CRUD операции вопросов и ответов
- ✅ Валидацию входных данных
- ✅ Обработку ошибок (404, 422)
- ✅ Пагинацию и фильтрацию
- ✅ Каскадное удаление

## 🔧 Настройка окружения

Файл `.env`:

```env
# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=qa_fastapi
DB_USER=postgres
DB_PWD=postgres

# PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

## 📊 Модели данных

### Question (Вопрос)
```python
id: int (autoincrement)
text: str (255) - текст вопроса
created_at: datetime
```

### Answer (Ответ)
```python
id: int (autoincrement)
question_id: int (ForeignKey, CASCADE delete)
user_id: str (36) - UUID пользователя
text: str (255) - текст ответа
created_at: datetime
```

## 🐛 Troubleshooting

### Распространенные проблемы

**Ошибка подключения к БД:**
```bash
# Проверьте что PostgreSQL контейнер запущен
docker-compose ps

# Просмотр логов БД
docker-compose logs db
```

**Проблемы с миграциями:**
```bash
# Принудительное применение миграций
docker-compose exec app alembic upgrade head
```

**Очистка и перезапуск:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🔄 Миграции БД

### Создание новой миграции
```bash
docker-compose exec app alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций
```bash
docker-compose exec app alembic upgrade head
```

### Откат миграции
```bash
docker-compose exec app alembic downgrade -1
```

## 🤝 Разработка

### Локальная разработка

1. **Установите зависимости:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2. **Запустите БД:**
```bash
docker-compose up db -d
```

3. **Запустите приложение:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📄 Соответствие ТЗ

| Требование | Статус | Примечания |
|-----------|--------|------------|
| Модели Question и Answer | ✅ | Все поля соответствуют ТЗ |
| CRUD API для вопросов | ✅ | Полная реализация |
| CRUD API для ответов | ✅ | Полная реализация |
| Валидация данных | ✅ | Pydantic с кастомными валидаторами |
| Каскадное удаление | ✅ | ON DELETE CASCADE |
 PostgreSQL + ORM | ✅ | SQLAlchemy 2.0 + asyncpg |
| Миграции | ✅ | Alembic с autogenerate |
| Docker | ✅ | Полная контейнеризация |
| Логирование | ✅ | Структурированные логи |
