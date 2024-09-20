"""Create order and update table

Revision ID: 49dd3f73c333
Revises: 4f1fa216ee10
Create Date: 2024-09-20 16:22:23.762031

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "49dd3f73c333"
down_revision: Union[str, None] = "4f1fa216ee10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу order
    op.create_table(
        "order",
        sa.Column("promocode", sa.String(), nullable=True),
        sa.Column(
            "create_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Создаем уникальный индекс для колонки user_id в таблице profile
    op.execute(
        sa.text(
            """
        CREATE INDEX idx_unique_user_id ON profile (user_id)
        """
        )
    )


def downgrade() -> None:
    # Удаляем уникальный индекс из таблицы profile
    op.execute(sa.text("DROP INDEX IF EXISTS idx_unique_user_id"))

    # Удаляем таблицу order
    op.drop_table("order")
