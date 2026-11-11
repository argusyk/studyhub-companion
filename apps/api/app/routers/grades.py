from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Grade, GradeStatus, Lab, Submission, SubmissionStatus
from app.schemas.grade import GradeIn, GradeOut
from app.services import grading
from app.config import get_settings
from zoneinfo import ZoneInfo

router = APIRouter(tags=["grades"])


@router.put("/submissions/{submission_id}/grade", response_model=GradeOut)
def put_grade(submission_id: int, body: GradeIn, db: Session = Depends(get_session)):
    sub = db.get(Submission, submission_id)
    if sub is None:
        raise HTTPException(404, "Здачу не знайдено")
    lab = db.get(Lab, sub.lab_id)
    try:
        criteria = [grading.CriterionScore(c.name, c.weight, c.score, c.max_score)
                    for c in body.criteria]
        raw = grading.raw_score(criteria)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    days = grading.late_days(sub.submitted_at, lab.deadline, ZoneInfo(get_settings().department_tz))
    percent = grading.late_penalty_percent(days)
    penalty = grading.penalty_points(raw, percent)
    final = grading.final_score(raw, penalty)

    grade = db.scalar(select(Grade).where(Grade.submission_id == submission_id))
    if grade is None:
        grade = Grade(submission_id=submission_id)
        db.add(grade)
    grade.raw_score, grade.late_days = float(raw), days
    grade.penalty_percent, grade.penalty = percent, float(penalty)
    grade.final_score = float(final)
    grade.status = GradeStatus.FINAL if body.publish else GradeStatus.DRAFT
    if body.publish:
        sub.score = grading.published_score(final)
        sub.status = SubmissionStatus.REVIEWED
    db.commit()
    db.refresh(grade)
    return grade


@router.get("/submissions/{submission_id}/grade", response_model=GradeOut)
def get_grade(submission_id: int, db: Session = Depends(get_session)):
    grade = db.scalar(select(Grade).where(Grade.submission_id == submission_id))
    if grade is None:
        raise HTTPException(404, "Оцінку не знайдено")
    return grade
