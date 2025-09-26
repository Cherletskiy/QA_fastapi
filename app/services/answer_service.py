from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundError
from app.logging_config import setup_logger
from app.repository.answer_repository import AnswerRepository
from app.schemes.answer_scheme import AnswerResponse, AnswerPaginationResponse, AnswerCreate

logger = setup_logger(__name__)


class AnswerService:
    def __init__(self, repository: AnswerRepository):
        self.repository = repository

    async def create_answer(self, question_id: int, answer_data: AnswerCreate, session: AsyncSession) -> AnswerResponse:
        db_answer = await self.repository.create(question_id, answer_data, session)
        return AnswerResponse.model_validate(db_answer)

    async def get_answers(self, session: AsyncSession, question_id: int,
                          offset: int = 0, limit: int = 10) -> AnswerPaginationResponse:
        db_answers, total_count = await self.repository.get_by_question_id(session, question_id)

        answers = [AnswerResponse.model_validate(answer) for answer in db_answers]

        return AnswerPaginationResponse(
            total=total_count,
            items=answers,
            limit=limit,
            offset=offset
        )

    async def get_answer(self, answer_id: int, session: AsyncSession) -> AnswerResponse:
        db_answer = await self.repository.get_by_id(answer_id, session)
        if not db_answer:
            raise NotFoundError(f"Answer with id {answer_id} not found")
        return AnswerResponse.model_validate(db_answer)

    async def delete_answer(self, answer_id: int, session: AsyncSession) -> None:
        db_answer = await self.repository.get_by_id(answer_id, session)
        if not db_answer:
            raise NotFoundError(f"Answer with id {answer_id} not found")
        await self.repository.delete(db_answer, session)


