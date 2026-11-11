from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Grade, Lab, Student, Submission


class UnknownGroup(Exception):
    pass


def _rows(db: Session, group: str):
    if db.scalar(select(Student.id).where(Student.group_code == group).limit(1)) is None:
        raise UnknownGroup(group)
    stmt = (
        select(Student.full_name, Lab.number, Grade, Submission)
        .join(Submission, Submission.student_id == Student.id)
        .join(Lab, Lab.id == Submission.lab_id)
        .join(Grade, Grade.submission_id == Submission.id)
        .where(Student.group_code == group)
    )
    return sorted(db.execute(stmt).all(), key=lambda r: (r[0], r[1]))


def _num(value: float) -> int | float:
    return int(value) if float(value).is_integer() else value


def group_grades(db: Session, group: str) -> dict:
    grades = [
        {"student": name, "lab": number, "raw": _num(g.raw_score),
         "final": sub.score, "late_days": g.late_days}
        for name, number, g, sub in _rows(db, group)
    ]
    return {"group": group, "grades": grades}


def group_stats(db: Session, group: str) -> dict:
    rows = _rows(db, group)
    scores = [sub.score for _, _, _, sub in rows if sub.score is not None]
    return {
        "group": group,
        "submissions": len(rows),
        "avg_final": round(sum(scores) / len(scores), 2) if scores else 0,
        "late_count": sum(1 for _, _, g, _ in rows if g.late_days > 0),
    }
