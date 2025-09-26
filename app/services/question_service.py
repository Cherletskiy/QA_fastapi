from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundError
from app.schemes.question_scheme import QuestionCreate, QuestionResponse, PaginatedQuestionsResponse, \
    QuestionAnswerResponse
from app.repository.question_repository import QuestionRepository
from app.services.answer_service import AnswerService


class QuestionService:
    def __init__(self, repository: QuestionRepository, answer_service: AnswerService):
        self.repository = repository
        self.answer_service = answer_service

    async def create_question(self, question_data: QuestionCreate, session: AsyncSession) -> QuestionResponse:
        db_question = await self.repository.create(question_data, session)
        return QuestionResponse.model_validate(db_question)

    async def get_question(
            self,
            question_id: int,
            session: AsyncSession,
            limit: int = 10,
            offset: int = 0,
    ) -> QuestionAnswerResponse:
        db_question = await self.repository.get_by_id(session=session, question_id=question_id)
        if not db_question:
            raise NotFoundError(f"Question with id={question_id} not found")

        answers_page = await self.answer_service.get_answers(session=session, question_id=question_id, limit=limit,
                                                             offset=offset)

        return QuestionAnswerResponse(
            id=db_question.id,
            text=db_question.text,
            created_at=db_question.created_at,
            answers=answers_page
        )

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