from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    name: Mapped[str] = mapped_column(
        String(20),  # Ограничивает длинну строки
        unique=True,
    )  # mapped_column(unique=True) - уникальность

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(uselist=False, back_populates="user")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}  {self.id} {self.name}"

    def __repr__(self) -> str:
        return str(self)
