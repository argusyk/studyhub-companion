from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Grade, Submission
from app.services import groups as service

router = APIRouter(tags=["groups"])


@router.get("/groups/{group}/grades")
def group_grades(group: str, db: Session = Depends(get_session)):
    try:
        return service.group_grades(db, group)
    except service.UnknownGroup as exc:
        raise HTTPException(404, "Групу не знайдено") from exc


@router.get("/groups/{group}/stats")
def group_stats(group: str, db: Session = Depends(get_session)):
    try:
        return service.group_stats(db, group)
    except service.UnknownGroup as exc:
        raise HTTPException(404, "Групу не знайдено") from exc


@router.get("/submissions/{submission_id}/score")
def submission_score(submission_id: int, db: Session = Depends(get_session)):
    sub = db.get(Submission, submission_id)
    grade = db.query(Grade).filter(Grade.submission_id == submission_id).one_or_none()
    if sub is None or grade is None:
        raise HTTPException(404, "Здачу не знайдено")
    raw = grade.raw_score
    return {"id": submission_id, "raw": int(raw) if float(raw).is_integer() else raw,
            "final": sub.score, "late_days": grade.late_days}
