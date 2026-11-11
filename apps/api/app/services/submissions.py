from sqlalchemy.orm import Session

from app import storage
from app.models import Lab, Student, Submission
from app.schemas.submission import SubmissionCreate


class NotFound(Exception):
    """Лабораторної або студента немає."""


def create_submission(db: Session, lab_id: int, payload: SubmissionCreate, data: bytes) -> Submission:
    if db.get(Lab, lab_id) is None:
        raise NotFound(f"lab {lab_id}")
    if db.get(Student, payload.student_id) is None:
        raise NotFound(f"student {payload.student_id}")
    path = storage.save_upload(lab_id, payload.student_id, payload.filename, data)
    sub = Submission(
        lab_id=lab_id,
        student_id=payload.student_id,
        file_url=path.as_posix(),
        filename=payload.filename,
        size_bytes=len(data),
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub
