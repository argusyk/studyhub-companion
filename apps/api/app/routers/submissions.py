from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Submission
from app.schemas.submission import MAX_UPLOAD_BYTES, SubmissionCreate, SubmissionOut
from app.services import submissions as service

router = APIRouter(tags=["submissions"])


@router.post("/labs/{lab_id}/submissions", response_model=SubmissionOut, status_code=201)
def submit_lab(
    lab_id: int,
    # Навчальне спрощення: у реальному сервісі student_id береться з токена, а не з форми.
    student_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_session),
):
    data = file.file.read(MAX_UPLOAD_BYTES + 1)
    if not data:
        raise HTTPException(400, "Порожній файл")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Файл більший за 10 МБ")
    try:
        payload = SubmissionCreate(student_id=student_id, filename=file.filename or "",
                                   size_bytes=len(data))
    except ValidationError as exc:
        raise HTTPException(422, exc.errors(include_url=False, include_context=False)) from exc
    try:
        return service.create_submission(db, lab_id, payload, data)
    except service.NotFound as exc:
        raise HTTPException(404, "Лабораторну або студента не знайдено") from exc


@router.get("/submissions/{submission_id}", response_model=SubmissionOut)
def get_submission(submission_id: int, db: Session = Depends(get_session)):
    sub = db.get(Submission, submission_id)
    if sub is None:
        raise HTTPException(404, "Здачу не знайдено")
    return sub
