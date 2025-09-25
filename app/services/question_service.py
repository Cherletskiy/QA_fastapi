from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundError
from app.schemes.question_scheme import QuestionCreate, QuestionResponse, PaginatedQuestionsResponse
from app.repository.question_repository import QuestionRepository


class QuestionService:
    def __init__(self, repository: QuestionRepository):
        self.repository = repository

    async def create_question(self, question_data: QuestionCreate, session: AsyncSession) -> QuestionResponse:
        db_question = await self.repository.create(question_data, session)
        return QuestionResponse.model_validate(db_question)

    async def get_question(self, question_id: int, session: AsyncSession) -> QuestionResponse:
        db_question = await self.repository.get_by_id(question_id, session)
        if not db_question:
            raise NotFoundError(f"Question with id {question_id} not found")
        return QuestionResponse.model_validate(db_question)

    async def get_all_questions(self, session: AsyncSession,
                                offset: int = 0, limit: int = 10) -> PaginatedQuestionsResponse:
        db_questions, total = await self.repository.get_all(session=session, limit=limit, offset=offset)
        questions = [QuestionResponse.model_validate(question) for question in db_questions]

        return PaginatedQuestionsResponse(
            total=total,
            items=questions,
            limit=limit,
            offset=offset
        )

    async def delete_question(self, question_id: int, session: AsyncSession) -> None:
        db_question = await self.repository.get_by_id(question_id, session)
        if not db_question:
            raise NotFoundError(f"Question with id {question_id} not found")
        await self.repository.delete(db_question, session)