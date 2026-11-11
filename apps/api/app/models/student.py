from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    # Група як slug, що використовується в URL: "ki-21", "pi-22a".
    group_code: Mapped[str] = mapped_column(String(20), index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
