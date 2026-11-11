from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app import storage
from app.models import Lab, Student, Submission
from app.schemas.submission import SubmissionCreate
from app.services.deadlines import is_late


class NotFound(Exception):
    """Лабораторної або студента немає."""


def mark_submission(submission: Submission, lab: Lab) -> None:
    """Позначає здачу як запізнілу: порівнюються лише aware-значення (UTC)."""
    submission.is_late = is_late(submission.submitted_at, lab.deadline)


def create_submission(db: Session, lab_id: int, payload: SubmissionCreate, data: bytes) -> Submission:
    lab = db.get(Lab, lab_id)
    if lab is None:
        raise NotFound(f"lab {lab_id}")
    if db.get(Student, payload.student_id) is None:
        raise NotFound(f"student {payload.student_id}")
    path = storage.save_upload(lab_id, payload.student_id, payload.filename, data)
    sub = Submission(
        lab_id=lab_id,
        student_id=payload.student_id,
        submitted_at=datetime.now(timezone.utc),
        file_url=path.as_posix(),
        filename=payload.filename,
        size_bytes=len(data),
    )
    mark_submission(sub, lab)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub
