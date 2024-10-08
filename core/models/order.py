from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .order_product_association import OrderProductAssociation

if TYPE_CHECKING:
    from .product import Product


class Order(Base):
    promocode: Mapped[str | None]
    create_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )

    products: Mapped[list["Product"]] = relationship(
        secondary="order_product_association",
        back_populates="orders",
    )
