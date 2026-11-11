"""Завантаження seed-даних: `python -m app.seed [--reset]`. Лише вигадані дані."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import Base
from app.db.session import get_engine
from app.models import Lab, Student

SEED_DIR = Path(__file__).resolve().parents[3] / "data" / "seed"


def _utc(local_iso: str) -> datetime:
    """Дедлайн за часом кафедри -> UTC (aware)."""
    tz = ZoneInfo(get_settings().department_tz)
    return datetime.fromisoformat(local_iso).replace(tzinfo=tz).astimezone(timezone.utc)


def load_seed(session: Session, seed_dir: Path = SEED_DIR) -> tuple[int, int]:
    students = json.loads((seed_dir / "students.json").read_text("utf-8"))
    labs = json.loads((seed_dir / "labs.json").read_text("utf-8"))
    session.add_all(Student(**s) for s in students)
    session.add_all(
        Lab(number=x["number"], title=x["title"], deadline=_utc(x["deadline_local"]),
            max_score=x.get("max_score", 100))
        for x in labs
    )
    session.commit()
    return len(students), len(labs)


def main() -> None:
    engine = get_engine()
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        if "--reset" in sys.argv:
            session.execute(delete(Lab))
            session.execute(delete(Student))
            session.commit()
        print("seed: students=%d labs=%d" % load_seed(session))


if __name__ == "__main__":
    main()
