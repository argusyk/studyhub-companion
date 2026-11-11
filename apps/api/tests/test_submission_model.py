import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Submission, SubmissionStatus
from app.seed import load_seed


def _make(**kw):
    base = dict(student_id=1, lab_id=1, file_url="uploads/1/1/report.pdf",
                filename="report.pdf", size_bytes=10)
    return Submission(**(base | kw))


def test_defaults(db):
    load_seed(db)
    sub = _make()
    db.add(sub)
    db.commit()
    assert sub.status is SubmissionStatus.SUBMITTED
    assert sub.score is None
    assert sub.submitted_at.tzinfo is not None


@pytest.mark.parametrize("score", [-1, 101])
def test_score_out_of_range_rejected_by_db(db, score):
    load_seed(db)
    db.add(_make(score=score))
    with pytest.raises(IntegrityError):
        db.commit()


@pytest.mark.parametrize("score", [0, 100])
def test_score_boundaries_accepted(db, score):
    load_seed(db)
    db.add(_make(score=score))
    db.commit()
