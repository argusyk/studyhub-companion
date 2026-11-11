from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.grade import GradeStatus


class CriterionIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    weight: Decimal = Field(gt=0, le=100)
    score: Decimal = Field(ge=0)
    max_score: Decimal = Field(gt=0)


class GradeIn(BaseModel):
    criteria: list[CriterionIn] = Field(min_length=1)
    publish: bool = False


class GradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    submission_id: int
    raw_score: float
    late_days: int
    penalty_percent: int
    penalty: float
    final_score: float
    status: GradeStatus
