from sqlalchemy import func, select

from app.models import Lab, Student
from app.seed import load_seed


def test_seed_counts(db):
    assert load_seed(db) == (8, 6)
    assert db.scalar(select(func.count()).select_from(Student)) == 8
    assert db.scalar(select(func.count()).select_from(Lab)) == 6
