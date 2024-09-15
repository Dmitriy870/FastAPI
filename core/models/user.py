from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    name: Mapped[str] = mapped_column(
        String(20),  # Ограничивает длинну строки
        unique=True,
    )  # mapped_column(unique=True) - уникальность

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")
