from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Question
from app.errors import ConflictError
from app.schemes.question_scheme import QuestionCreate
from app.logging_config import setup_logger


logger = setup_logger(__name__)


class QuestionRepository:

    async def create(self, question_data: QuestionCreate, session: AsyncSession) -> Question:
        db_question = Question(text=question_data.text)
        session.add(db_question)
        try:
            await session.commit()
            await session.refresh(db_question)
            return db_question
        except IntegrityError as e:
            await session.rollback()
            raise ConflictError("Can't create question") from e

    async def get_by_id(self, question_id: int, session: AsyncSession) -> Question | None:
        return await session.get(Question, question_id)

    async def get_all(self, session: AsyncSession,
                      offset: int = 0, limit: int = 100) -> tuple[list[Question], int]:
            limit = min(limit, 100)
            offset = max(offset, 0)

            stmt = select(Question).offset(offset).limit(limit)
            result = await session.execute(stmt)
            questions_list = result.scalars().all()

            total_count = await session.scalar(select(func.count(Question.id)))

            return questions_list, total_count

    async def delete(self, db_question: Question, session: AsyncSession) -> None:
        try:
            await session.delete(db_question)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ConflictError("Can't delete question") from e


