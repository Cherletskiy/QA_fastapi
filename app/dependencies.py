from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import async_session_factory
from app.repository.answer_repository import AnswerRepository
from app.repository.question_repository import QuestionRepository
from app.services.answer_service import AnswerService
from app.services.question_service import QuestionService
from app.logging_config import setup_logger


logger = setup_logger(__name__)


def get_answer_service() -> AnswerService:
    return AnswerService(repository=AnswerRepository())


def get_question_service(
    answer_service: AnswerService = Depends(get_answer_service),
) -> QuestionService:
    return QuestionService(
        repository=QuestionRepository(),
        answer_service=answer_service,
    )


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Error in async session: {e}")
            raise
        finally:
            await session.close()