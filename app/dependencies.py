from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import async_session_factory
from app.repository.question_repository import QuestionRepository
from app.services.question_service import QuestionService


def get_question_service() -> QuestionService:
    return QuestionService(repository=QuestionRepository())


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()