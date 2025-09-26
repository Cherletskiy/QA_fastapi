from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_async_session
from app.dependencies import get_question_service
from app.schemes.question_scheme import QuestionCreate, QuestionResponse, PaginationParams, QuestionAnswerResponse
from app.services.question_service import QuestionService
from app.schemes.question_scheme import PaginatedQuestionsResponse


router = APIRouter(prefix="/api/v1/questions", tags=["questions"])


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED,
             summary="Create question")
async def create_question(
    question: QuestionCreate,
    session: AsyncSession = Depends(get_async_session),
    service: QuestionService = Depends(get_question_service),
):
    return await service.create_question(question, session)


@router.get("/{question_id}", response_model=QuestionAnswerResponse, summary="Get question by id with answers")
async def get_question(
    question_id: int,
    pagination: PaginationParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
    service: QuestionService = Depends(get_question_service),
):
    return await service.get_question(
        question_id=question_id,
        session=session,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/", response_model=PaginatedQuestionsResponse, summary="Get all questions with pagination")
async def get_questions(
    pagination: PaginationParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
    service: QuestionService = Depends(get_question_service),
):
    return await service.get_all_questions(
        session,
        offset=pagination.offset,
        limit=pagination.limit
    )


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete question by id")
async def delete_question(
    question_id: int,
    session: AsyncSession = Depends(get_async_session),
    service: QuestionService = Depends(get_question_service),
):
    await service.delete_question(question_id, session)

