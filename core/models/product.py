from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import Mapped, relationship
from .order_product_association import OrderProductAssociation

if TYPE_CHECKING:
    from .order import Order


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(
        secondary="order_product_association",
        back_populates="products",
    )
