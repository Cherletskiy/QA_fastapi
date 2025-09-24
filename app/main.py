from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.db import init_db, close_db
from app.logging_config import setup_logger


# Настройка логирования
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    logger.info("Запуск приложения: инициализация БД")
    await init_db()
    logger.info("Приложение запущено")

    try:
        yield
    finally:
        logger.info("Остановка приложения: закрытие БД")
        await close_db()
        logger.info("Приложение остановлено")


# Создание приложения
app = FastAPI(
    title="QA API",
    description="API для управления задачами",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
