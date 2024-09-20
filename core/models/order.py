from datetime import datetime

from sqlalchemy import func

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Order(Base):
    promocode: Mapped[str | None]
    create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
