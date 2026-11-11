"""Збереження завантажених файлів. Ім'я файлу вже перевірене схемою SubmissionCreate."""
from pathlib import Path

from app.config import get_settings

UPLOAD_ROOT = Path(get_settings().upload_dir)


def save_upload(lab_id: int, student_id: int, filename: str, data: bytes) -> Path:
    target_dir = UPLOAD_ROOT / str(lab_id) / str(student_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / filename
    # Захист від виходу за межі каталогу навіть якщо валідацію колись послаблять.
    if UPLOAD_ROOT.resolve() not in path.resolve().parents:
        raise ValueError("шлях виходить за межі каталогу завантажень")
    path.write_bytes(data)
    return path
