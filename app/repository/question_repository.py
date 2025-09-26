from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Question
from app.errors import ConflictError
from app.schemes.question_scheme import QuestionCreate
from app.logging_config import setup_logger

logger = setup_logger(__name__)


class QuestionRepository:
    """Repository for question operations."""

    async def create(self, question_data: QuestionCreate, session: AsyncSession) -> Question:
        """
        Create a new question.

        Args:
            question_data: Question creation data
            session: Database session

        Returns:
            Created question object

        Raises:
            ConflictError: If question creation fails
        """
        logger.info("Creating new question")

        db_question = Question(text=question_data.text)
        session.add(db_question)
        try:
            await session.commit()
            await session.refresh(db_question)
            logger.info(f"Question {db_question.id} created successfully")
            return db_question
        except IntegrityError as e:
            await session.rollback()
            logger.error(f"Integrity error creating question: {e}")
            raise ConflictError("Can't create question") from e

    async def get_by_id(self, question_id: int, session: AsyncSession) -> Question | None:
        """
        Get question by ID.

        Args:
            question_id: ID of the question to retrieve
            session: Database session

        Returns:
            Question object or None if not found
        """
        logger.debug(f"Retrieving question by ID: {question_id}")
        question = await session.get(Question, question_id)
        if question:
            logger.debug(f"Question {question_id} found")
        else:
            logger.debug(f"Question {question_id} not found")
        return question

    async def get_all(self, session: AsyncSession,
                      offset: int = 0, limit: int = 100) -> tuple[list[Question], int]:
        """
        Get all questions with pagination.

        Args:
            session: Database session
            offset: Number of questions to skip
            limit: Maximum number of questions to return (max 100)

        Returns:
            Tuple of (list of questions, total count)
        """
        logger.debug(f"Retrieving all questions, limit: {limit}, offset: {offset}")

        limit = min(limit, 100)
        offset = max(offset, 0)

        stmt = select(Question).offset(offset).limit(limit)
        result = await session.execute(stmt)
        questions_list = result.scalars().all()

        total_count = await session.scalar(select(func.count(Question.id)))
        total_count = int(total_count or 0)

        logger.debug(f"Found {len(questions_list)} questions, total: {total_count}")
        return questions_list, total_count

    async def delete(self, db_question: Question, session: AsyncSession) -> None:
        """
        Delete a question.

        Args:
            db_question: Question object to delete
            session: Database session

        Raises:
            ConflictError: If question deletion fails
        """
        logger.info(f"Deleting question {db_question.id}")

        try:
            await session.delete(db_question)
            await session.commit()
            logger.info(f"Question {db_question.id} deleted successfully")
        except IntegrityError as e:
            await session.rollback()
            logger.error(f"Integrity error deleting question {db_question.id}: {e}")
            raise ConflictError("Can't delete question") from e