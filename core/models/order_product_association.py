from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from core.models import Base
import sqlalchemy as sa
from alembic import op

order_product_association_table = Table(
    "OrderProductAssociationTable",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("product_id", ForeignKey("product.id"), nullable=False, unique=True),
    Column("order_id", ForeignKey("order.id"), nullable=False, unique=True),
    UniqueConstraint("product_id", "order_id", name="index_unique_prod_order"),
)
