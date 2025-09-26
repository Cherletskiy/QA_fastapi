from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_async_session, get_answer_service
from app.schemes.answer_scheme import AnswerResponse, AnswerCreate
from app.services.answer_service import AnswerService


router = APIRouter(prefix="/api/v1", tags=["answers"], redirect_slashes=False)


@router.post("/questions/{question_id}/answers", response_model=AnswerResponse, status_code=status.HTTP_201_CREATED, summary="Create answer")
async def create_answer(
    question_id: int,
    answer: AnswerCreate,
    session: AsyncSession = Depends(get_async_session),
    service: AnswerService = Depends(get_answer_service),
):
    return await service.create_answer(question_id, answer, session)


@router.get("/answers/{answer_id}", response_model=AnswerResponse, summary="Get answer by id")
async def get_answer(
        answer_id: int,
        session: AsyncSession = Depends(get_async_session),
        service: AnswerService = Depends(get_answer_service)
):
    return await service.get_answer(answer_id, session)


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete answer by id")
async def delete_answer(
    answer_id: int,
    session: AsyncSession = Depends(get_async_session),
    service: AnswerService = Depends(get_answer_service),
):
    await service.delete_answer(answer_id, session)