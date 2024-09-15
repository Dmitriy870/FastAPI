from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, mapped_column, relationship, Mapped


class UserRelationMixin:
    _user_back_populates: str | None = None
    _user_id_unique: bool = False

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("user.id"), unique=cls._user_id_unique)

    @declared_attr
    def user(cls):
        return relationship("User", back_populates=cls._user_back_populates)
