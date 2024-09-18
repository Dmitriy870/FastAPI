from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .mixins import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _user_back_populates = "profile"
    _user_id_unique = True
    first_name: Mapped[str | None] = mapped_column(
        String(20),  # Ограничивает длинну строки
    )  # mapped_column(unique=True) - уникальность
    last_name: Mapped[str | None] = mapped_column(String(20))
    bio: Mapped[str | None]
