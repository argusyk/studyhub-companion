from datetime import datetime
from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.submission import SubmissionStatus

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".zip", ".docx", ".md", ".py", ".txt"}


class SubmissionCreate(BaseModel):
    student_id: int = Field(gt=0)
    filename: str = Field(min_length=1, max_length=255)
    size_bytes: int = Field(gt=0, le=MAX_UPLOAD_BYTES)

    @field_validator("filename")
    @classmethod
    def safe_filename(cls, value: str) -> str:
        if any(sep in value for sep in ("/", "\\", "\x00")) or value in {".", ".."}:
            raise ValueError("ім'я файлу не може містити шляху")
        if PurePosixPath(value).suffix.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError("недозволене розширення файлу")
        return value


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    lab_id: int
    submitted_at: datetime
    file_url: str
    filename: str
    size_bytes: int
    status: SubmissionStatus
    score: int | None = Field(default=None, ge=0, le=100)
    is_late: bool = False
