import pytest
from pydantic import ValidationError

from app.schemas.submission import MAX_UPLOAD_BYTES, SubmissionCreate


def test_valid():
    s = SubmissionCreate(student_id=1, filename="report.pdf", size_bytes=1)
    assert s.filename == "report.pdf"


@pytest.mark.parametrize("size", [0, -1, MAX_UPLOAD_BYTES + 1])
def test_bad_size(size):
    with pytest.raises(ValidationError):
        SubmissionCreate(student_id=1, filename="a.pdf", size_bytes=size)


def test_size_upper_boundary_ok():
    SubmissionCreate(student_id=1, filename="a.pdf", size_bytes=MAX_UPLOAD_BYTES)


@pytest.mark.parametrize("name", ["../etc/passwd", "a/b.pdf", "a\\b.pdf", "..", "x.exe", "noext"])
def test_bad_filename(name):
    with pytest.raises(ValidationError):
        SubmissionCreate(student_id=1, filename=name, size_bytes=5)
