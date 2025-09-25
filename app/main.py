from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.database.db import init_db, close_db
from app.logging_config import setup_logger
from app.routes import question_routes
from app.errors import AppError


# Настройка логирования
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    logger.info("Starting application")
    await init_db()
    logger.info("Application started")

    try:
        yield
    finally:
        logger.info("Stopping application")
        await close_db()
        logger.info("Application stopped")


# Создание приложения
app = FastAPI(
    title="QA API",
    description="API-сервис для вопросов и ответов",
    version="1.0.0",
    lifespan=lifespan
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.warning(f"AppError {exc.code}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "internal_error", "message": "Internal server error"}}
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Регистрация маршрутов
app.include_router(question_routes.router)