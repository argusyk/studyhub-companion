import enum
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UtcDateTime


class SubmissionStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    REVIEWED = "reviewed"
    RETURNED = "returned"


class Submission(Base):
    """Канонічна модель здачі (єдина для всього посібника, див. companion-notes)."""

    __tablename__ = "submissions"
    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 100", name="ck_submission_score"),
        CheckConstraint("size_bytes > 0", name="ck_submission_size"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), index=True)
    lab_id: Mapped[int] = mapped_column(ForeignKey("labs.id"), index=True)
    submitted_at: Mapped[datetime] = mapped_column(UtcDateTime(), server_default=func.now())
    file_url: Mapped[str] = mapped_column(String(512))
    filename: Mapped[str] = mapped_column(String(255))
    size_bytes: Mapped[int] = mapped_column(Integer)
    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(
            SubmissionStatus,
            name="submission_status",
            values_callable=lambda e: [m.value for m in e],
        ),
        default=SubmissionStatus.SUBMITTED,
    )
    # Підсумковий опублікований бал (ціле 0..100); джерело – Grade.final_score (розд. 8).
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Позначка «здано із запізненням», обчислюється при здачі (розд. 10).
    is_late: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
