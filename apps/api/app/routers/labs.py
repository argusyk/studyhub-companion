from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Lab
from app.schemas.lab import LabOut

router = APIRouter(prefix="/labs", tags=["labs"])


@router.get("", response_model=list[LabOut])
def list_labs(
    q: str | None = Query(None, min_length=1, max_length=100, description="Пошук у назві"),
    deadline_before: datetime | None = Query(None, description="Лише з дедлайном до (aware)"),
    deadline_after: datetime | None = Query(None, description="Лише з дедлайном після (aware)"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session),
):
    for name, value in (("deadline_before", deadline_before), ("deadline_after", deadline_after)):
        if value is not None and value.tzinfo is None:
            raise HTTPException(422, f"{name} має містити часовий пояс (наприклад, Z)")
    stmt = select(Lab).order_by(Lab.number)
    if q:
        stmt = stmt.where(Lab.title.ilike(f"%{q}%"))
    if deadline_before:
        stmt = stmt.where(Lab.deadline < deadline_before)
    if deadline_after:
        stmt = stmt.where(Lab.deadline > deadline_after)
    return db.scalars(stmt.limit(limit).offset(offset)).all()


@router.get("/{lab_id}", response_model=LabOut)
def get_lab(lab_id: int, db: Session = Depends(get_session)):
    lab = db.get(Lab, lab_id)
    if lab is None:
        raise HTTPException(404, "Лабораторну не знайдено")
    return lab
