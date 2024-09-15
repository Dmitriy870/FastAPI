from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    username: Mapped[str] = mapped_column(
        String(20),  # Ограничивает длинну строки
        unique=True,
    )  # mapped_column(unique=True) - уникальность
