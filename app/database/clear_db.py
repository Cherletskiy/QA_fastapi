import asyncio
from app.database.db import engine
from app.database.models import Base


async def clear_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Таблицы удалены")

asyncio.run(clear_db())