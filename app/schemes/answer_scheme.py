from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime
from uuid import UUID


class AnswerCreate(BaseModel):
    user_id: str = Field(..., description="User UUID")
    text: str

    @field_validator("user_id")
    def validate_uuid_format(cls, v: str) -> str:
        try:
            UUID(v, version=4)
        except ValueError:
            raise ValueError("user_id must be a valid UUID version 4")
        return v

    @field_validator("text")
    def text_not_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Текст ответа не может быть пустым")
        return v

    model_config = ConfigDict(extra="forbid")


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerPaginationResponse(BaseModel):
    total: int
    items: list[AnswerResponse]
    limit: int
    offset: int