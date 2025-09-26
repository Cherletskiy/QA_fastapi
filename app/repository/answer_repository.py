from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import ConflictError
from app.logging_config import setup_logger
from app.database.models import Answer
from app.schemes.answer_scheme import AnswerCreate

logger = setup_logger(__name__)


class AnswerRepository:

    async def create(self, question_id: int, answer_data: AnswerCreate, session: AsyncSession) -> Answer:
        answer = Answer(question_id=question_id, user_id=answer_data.user_id, text=answer_data.text)
        session.add(answer)
        try:
            await session.commit()
            await session.refresh(answer)
            return answer
        except IntegrityError as e:
            await session.rollback()
            raise ConflictError("Can't create answer") from e

    async def get_by_id(self, answer_id: int, session: AsyncSession) -> Answer | None:
        return await session.get(Answer, answer_id)

    async def get_by_question_id(
            self,
            session: AsyncSession,
            question_id: int,
            limit: int = 10,
            offset: int = 0,
    ) -> tuple[list[Answer], int]:
        limit = min(limit, 100)
        offset = max(offset, 0)

        stmt = select(Answer).where(Answer.question_id == question_id).offset(offset).limit(limit)
        result = await session.execute(stmt)
        answers_list = result.scalars().all()

        total_count = await session.scalar(
            select(func.count(Answer.id)).where(Answer.question_id == question_id)
        )
        total_count = int(total_count or 0)

        return answers_list, total_count

    async def delete(self, db_answer: Answer, session: AsyncSession) -> None:
        try:
            await session.delete(db_answer)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ConflictError("Can't delete answer") from e