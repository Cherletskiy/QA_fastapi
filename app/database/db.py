from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.logging_config import setup_logger
from app.database.models import Base


# Настройка логирования
logger = setup_logger(__name__)

# Загрузка переменных окружения
load_dotenv()

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "database": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


DSN = (f"postgresql+asyncpg://{DATABASE_CONFIG["user"]}:{DATABASE_CONFIG["password"]}@"
       f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}")

engine = create_async_engine(
    url=DSN,
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession
)





async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")


async def close_db():
    await engine.dispose()
    logger.info("Database closed")