import enum

from sqlalchemy import Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GradeStatus(str, enum.Enum):
    DRAFT = "draft"
    FINAL = "final"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id"), unique=True)
    raw_score: Mapped[float] = mapped_column(Float)
    late_days: Mapped[int] = mapped_column(Integer, default=0)
    penalty_percent: Mapped[int] = mapped_column(Integer, default=0)
    penalty: Mapped[float] = mapped_column(Float, default=0.0)
    final_score: Mapped[float] = mapped_column(Float)
    status: Mapped[GradeStatus] = mapped_column(
        Enum(GradeStatus, name="grade_status", values_callable=lambda e: [m.value for m in e]),
        default=GradeStatus.DRAFT,
    )
