from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import ConflictError, NotFoundError
from app.logging_config import setup_logger
from app.database.models import Answer
from app.schemes.answer_scheme import AnswerCreate

logger = setup_logger(__name__)


class AnswerRepository:
    """Repository for answer operations."""

    async def create(self, question_id: int, answer_data: AnswerCreate, session: AsyncSession) -> Answer:
        """
        Create a new answer for a question.

        Args:
            question_id: ID of the question to answer
            answer_data: Answer creation data
            session: Database session

        Returns:
            Created answer object

        Raises:
            NotFoundError: If question doesn't exist
            ConflictError: If answer creation fails
        """
        logger.info(f"Creating answer for question {question_id} by user {answer_data.user_id}")

        answer = Answer(question_id=question_id, user_id=answer_data.user_id, text=answer_data.text)
        session.add(answer)
        try:
            await session.commit()
            await session.refresh(answer)
            logger.info(f"Answer {answer.id} created successfully for question {question_id}")
            return answer
        except IntegrityError as e:
            await session.rollback()
            if e.orig.pgcode == "23503":
                logger.warning(f"Question {question_id} not found when creating answer")
                raise NotFoundError(f"question {question_id} not found") from e
            logger.error(f"Integrity error creating answer: {e}")
            raise ConflictError("Can't create answer") from e

    async def get_by_id(self, answer_id: int, session: AsyncSession) -> Answer | None:
        """
        Get answer by ID.

        Args:
            answer_id: ID of the answer to retrieve
            session: Database session

        Returns:
            Answer object or None if not found
        """
        logger.debug(f"Retrieving answer by ID: {answer_id}")
        answer = await session.get(Answer, answer_id)
        if answer:
            logger.debug(f"Answer {answer_id} found")
        else:
            logger.debug(f"Answer {answer_id} not found")
        return answer

    async def get_by_question_id(
            self,
            session: AsyncSession,
            question_id: int,
            limit: int = 10,
            offset: int = 0,
    ) -> tuple[list[Answer], int]:
        """
        Get answers for a specific question with pagination.

        Args:
            session: Database session
            question_id: ID of the question
            limit: Maximum number of answers to return (max 100)
            offset: Number of answers to skip

        Returns:
            Tuple of (list of answers, total count)
        """
        logger.debug(f"Retrieving answers for question {question_id}, limit: {limit}, offset: {offset}")

        limit = min(limit, 100)
        offset = max(offset, 0)

        stmt = select(Answer).where(Answer.question_id == question_id).offset(offset).limit(limit)
        result = await session.execute(stmt)
        answers_list = result.scalars().all()

        total_count = await session.scalar(
            select(func.count(Answer.id)).where(Answer.question_id == question_id)
        )
        total_count = int(total_count or 0)

        logger.debug(f"Found {len(answers_list)} answers for question {question_id}, total: {total_count}")
        return answers_list, total_count

    async def delete(self, db_answer: Answer, session: AsyncSession) -> None:
        """
        Delete an answer.

        Args:
            db_answer: Answer object to delete
            session: Database session

        Raises:
            ConflictError: If answer deletion fails
        """
        logger.info(f"Deleting answer {db_answer.id} for question {db_answer.question_id}")

        try:
            await session.delete(db_answer)
            await session.commit()
            logger.info(f"Answer {db_answer.id} deleted successfully")
        except IntegrityError as e:
            await session.rollback()
            logger.error(f"Integrity error deleting answer {db_answer.id}: {e}")
            raise ConflictError("Can't delete answer") from e
