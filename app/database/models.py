from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime

from app.logging_config import setup_logger

# Настройка логирования
logger = setup_logger(__name__)


class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {"id": self.id}


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    @property
    def dict(self):
        created_str = self.created_at.isoformat() if self.created_at else "unknown"
        return {
            "id": self.id,
            "text": self.text,
            "created_at": created_str
        }


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    text: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    question: Mapped["Question"] = relationship("Question", back_populates="answers")
    user: Mapped["User"] = relationship("User", back_populates="answers")

    @property
    def dict(self):
        created_str = self.created_at.isoformat() if self.created_at else "unknown"
        return {
            "id": self.id,
            "question_id": self.question_id,
            "user_id": self.user_id,
            "text": self.text,
            "created_at": created_str
        }

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="user")

    @property
    def dict(self):
        created_str = self.created_at.isoformat() if self.created_at else "unknown"
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": created_str
        }