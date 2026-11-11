"""Тестові дані з фікстури legacy-прототипу (для паритетних тестів ЛР10).

`seed_db(db)` завантажує legacy/tests/fixtures/group_ki21.json у нову схему; оцінки
розраховуються за НОВОЮ політикою (R-07), а не за legacy.
"""
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import Grade, GradeStatus, Lab, Student, Submission, SubmissionStatus
from app.services import grading
from app.services.deadlines import DEPARTMENT_TZ, is_late

FIXTURE = Path(__file__).resolve().parents[3] / "legacy" / "tests" / "fixtures" / "group_ki21.json"


def _utc(local: str) -> datetime:
    return datetime.strptime(local, "%Y-%m-%d %H:%M").replace(tzinfo=DEPARTMENT_TZ).astimezone(timezone.utc)


def seed_db(db: Session, fixture: Path = FIXTURE) -> None:
    data = json.loads(fixture.read_text("utf-8"))
    labs = {}
    for s in data["students"]:
        db.add(Student(id=s["id"], full_name=s["name"], group_code=s["group"],
                       email=f"s{s['id']}@example.test"))
    for x in data["labs"]:
        labs[x["id"]] = Lab(id=x["id"], number=x["num"], title=f"ЛР{x['num']}",
                            deadline=_utc(x["deadline"]), max_score=100)
        db.add(labs[x["id"]])
    db.flush()
    for x in data["submissions"]:
        lab = labs[x["lab_id"]]
        submitted = _utc(x["submitted"])
        raw = Decimal(x["score"])
        days = grading.late_days(submitted, lab.deadline, DEPARTMENT_TZ)
        percent = grading.late_penalty_percent(days)
        penalty = grading.penalty_points(raw, percent)
        final = grading.final_score(raw, penalty)
        sub = Submission(id=x["id"], student_id=x["student_id"], lab_id=x["lab_id"],
                         submitted_at=submitted, file_url="fixtures/report.pdf",
                         filename="report.pdf", size_bytes=1, status=SubmissionStatus.REVIEWED,
                         score=grading.published_score(final), is_late=is_late(submitted, lab.deadline))
        db.add(sub)
        db.flush()
        db.add(Grade(submission_id=sub.id, raw_score=float(raw), late_days=days,
                     penalty_percent=percent, penalty=float(penalty), final_score=float(final),
                     status=GradeStatus.FINAL))
    db.commit()
