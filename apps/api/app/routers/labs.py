from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Lab
from app.schemas.lab import LabOut

router = APIRouter(prefix="/labs", tags=["labs"])


@router.get("", response_model=list[LabOut])
def list_labs(db: Session = Depends(get_session)):
    return db.scalars(select(Lab).order_by(Lab.number)).all()


@router.get("/{lab_id}", response_model=LabOut)
def get_lab(lab_id: int, db: Session = Depends(get_session)):
    lab = db.get(Lab, lab_id)
    if lab is None:
        raise HTTPException(404, "Лабораторну не знайдено")
    return lab
