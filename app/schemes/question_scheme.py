from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime

from app.schemes.answer_scheme import AnswerPaginationResponse


class QuestionCreate(BaseModel):
    text: str

    @field_validator("text")
    def text_not_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Текст вопроса не может быть пустым")
        return v

    model_config = ConfigDict(extra="forbid")


class QuestionResponse(BaseModel):
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginationParams(BaseModel):
    offset: int = Field(0, ge=0, description="Offset for pagination")
    limit: int = Field(10, ge=1, le=100, description="Limit for pagination, max 100")

    model_config = ConfigDict(from_attributes=True)


class PaginatedQuestionsResponse(BaseModel):
    total: int
    items: list[QuestionResponse]
    limit: int
    offset: int


class QuestionAnswerResponse(QuestionResponse):
    answers: AnswerPaginationResponse