from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import async_session_factory
from app.repository.answer_repository import AnswerRepository
from app.repository.question_repository import QuestionRepository
from app.services.answer_service import AnswerService
from app.services.question_service import QuestionService


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
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()