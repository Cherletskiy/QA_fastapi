from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime


class AnswerCreate(BaseModel):
    user_id: int
    text: str

    @field_validator("text")
    def text_not_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Текст ответа не может быть пустым")
        return v

    model_config = ConfigDict(extra="forbid")


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerPaginationResponse(BaseModel):
    total: int
    items: list[AnswerResponse]
    limit: int
    offset: int