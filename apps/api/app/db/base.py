from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Спільна база ORM-моделей. Нові моделі імпортуються в app/models/__init__.py."""
